param(
  [string]$ScriptPath,
  [string]$ManifestPath,
  [string]$PayloadPath,
  [string]$ManifestValidatorPath,
  [switch]$FailOnWarning
)

$ErrorActionPreference = 'Stop'
$script:report = [ordered]@{
  state = 'FAIL_OFFLINE_PREFLIGHT'
  script = $ScriptPath
  manifest = $ManifestPath
  payload = $PayloadPath
  checks = [ordered]@{}
  errors = @()
  warnings = @()
}

function Add-Error([string]$Code,[string]$Message) {
  $script:report.errors += [ordered]@{code=$Code;message=$Message}
}

function Add-Warning([string]$Code,[string]$Message) {
  $script:report.warnings += [ordered]@{code=$Code;message=$Message}
}

function Resolve-InputFile([string]$Path,[string]$Label) {
  if([string]::IsNullOrWhiteSpace($Path)){ return $null }
  if(-not (Test-Path -LiteralPath $Path -PathType Leaf)){
    Add-Error 'FILE_NOT_FOUND' "$Label not found: $Path"
    return $null
  }
  return (Resolve-Path -LiteralPath $Path).Path
}

function Convert-ColumnToNumber([string]$Letters) {
  $value=0
  foreach($ch in $Letters.ToUpperInvariant().ToCharArray()){
    $value=$value*26+([int]$ch-[int][char]'A'+1)
  }
  return $value
}

function Get-RangeSize([string]$Address) {
  $clean=($Address -replace '\$','')
  if($clean.Contains('!')){$clean=$clean.Substring($clean.LastIndexOf('!')+1)}
  $m=[regex]::Match($clean,'^(?<c1>[A-Za-z]+)(?<r1>\d+)(?::(?<c2>[A-Za-z]+)(?<r2>\d+))?$')
  if(-not $m.Success){ return $null }
  $c1=Convert-ColumnToNumber $m.Groups['c1'].Value
  $c2=$(if($m.Groups['c2'].Success){Convert-ColumnToNumber $m.Groups['c2'].Value}else{$c1})
  $r1=[int]$m.Groups['r1'].Value
  $r2=$(if($m.Groups['r2'].Success){[int]$m.Groups['r2'].Value}else{$r1})
  return [ordered]@{rows=[math]::Abs($r2-$r1)+1;columns=[math]::Abs($c2-$c1)+1}
}

try {
  $resolvedScript=Resolve-InputFile $ScriptPath 'Automation script'
  if($null -ne $resolvedScript){
    $content=Get-Content -LiteralPath $resolvedScript -Raw -Encoding UTF8
    $tokens=$null;$parseErrors=$null
    [void][Management.Automation.Language.Parser]::ParseInput($content,[ref]$tokens,[ref]$parseErrors)
    foreach($e in @($parseErrors)){Add-Error 'POWERSHELL_PARSE' ("{0} at {1}" -f $e.Message,$e.Extent.StartLineNumber)}

    $lintRules=@(
      @('RETURN_ADHESION','\breturn(?=\$)','return is immediately followed by a variable'),
      @('THROW_ADHESION','\bthrow(?=["''])','throw is immediately followed by a quote'),
      @('HELPER_ADHESION','\b(?:Rel|Calc|Input)(?=\$)','helper command is immediately followed by a variable'),
      @('RANGE_PAYLOAD_ADHESION','''[^''\r\n]*''(?=\$[A-Za-z_])','quoted argument is immediately followed by a variable'),
      @('ADJACENT_COMMAND_STRINGS','\b(?:Set-Block|Format-Common|Sheet)\s+\$[A-Za-z_]\w*\s+''[^''\r\n]*''(?='')','command has adjacent quoted arguments')
    )
    foreach($rule in $lintRules){
      foreach($m in [regex]::Matches($content,$rule[1])){
        $line=1+($content.Substring(0,$m.Index).Split("`n").Count-1)
        Add-Error $rule[0] ("{0} at line {1}: {2}" -f $rule[2],$line,$m.Value)
      }
    }
    $report.checks.scriptParse=($parseErrors.Count -eq 0)
    $report.checks.scriptLint=($report.errors.Count -eq 0)
  } else {
    Add-Warning 'SCRIPT_NOT_PROVIDED' 'No automation script was provided for parse and adhesion checks.'
  }

  $resolvedManifest=Resolve-InputFile $ManifestPath 'Workbook manifest'
  if($null -ne $resolvedManifest){
    $validator=$ManifestValidatorPath
    if([string]::IsNullOrWhiteSpace($validator) -and -not [string]::IsNullOrWhiteSpace($PSScriptRoot)){$validator=Join-Path $PSScriptRoot 'validate_manifest.py'}
    if([string]::IsNullOrWhiteSpace($validator)){
      $codexRoot=$(if(-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)){$env:CODEX_HOME}else{Join-Path $env:USERPROFILE '.codex'})
      $validator=Join-Path $codexRoot 'skills\excel-edit\scripts\validate_manifest.py'
    }
    $python=Get-Command python -ErrorAction SilentlyContinue
    if(-not (Test-Path -LiteralPath $validator -PathType Leaf)){
      Add-Error 'MANIFEST_VALIDATOR_NOT_FOUND' "validate_manifest.py not found: $validator"
    } elseif($null -eq $python){
      Add-Error 'PYTHON_NOT_FOUND' 'python is required to validate the workbook manifest.'
    } else {
      $manifestOutput=& $python.Source $validator $resolvedManifest 2>&1
      $report.checks.manifestOutput=($manifestOutput -join "`n")
      if($LASTEXITCODE -ne 0){Add-Error 'MANIFEST_INVALID' 'validate_manifest.py rejected the manifest.'}else{$report.checks.manifest=$true}
    }
  } else {
    Add-Warning 'MANIFEST_NOT_PROVIDED' 'No workbook manifest was provided.'
  }

  $resolvedPayload=Resolve-InputFile $PayloadPath 'Compiled write payload'
  if($null -ne $resolvedPayload){
    $payload=Get-Content -LiteralPath $resolvedPayload -Raw -Encoding UTF8 | ConvertFrom-Json
    $operations=@($payload.operations)
    if($operations.Count -eq 0){Add-Error 'PAYLOAD_EMPTY' 'Payload contains no operations.'}
    $index=0
    foreach($op in $operations){
      $index++
      $label=$(if($op.sheet){"$($op.sheet)!$($op.range)"}else{"operation $index"})
      $size=Get-RangeSize ([string]$op.range)
      if($null -eq $size){Add-Error 'RANGE_INVALID' "$label has an unsupported A1 range.";continue}
      $rows=@($op.rows)
      if($rows.Count -ne $size.rows){Add-Error 'ROW_COUNT_MISMATCH' "$label targets $($size.rows) rows but payload has $($rows.Count)."}
      for($r=0;$r-lt$rows.Count;$r++){
        $cells=@($rows[$r])
        if($cells.Count -ne $size.columns){Add-Error 'COLUMN_COUNT_MISMATCH' "$label row $($r+1) targets $($size.columns) columns but payload has $($cells.Count)."}
      }
      foreach($sample in @($op.formula_samples)){
        foreach($token in @($sample.expected_tokens)){
          if(([string]$sample.formula).IndexOf([string]$token,[StringComparison]::Ordinal) -lt 0){Add-Error 'FORMULA_TOKEN_MISSING' "$label formula sample is missing token: $token"}
        }
      }
    }
    $report.checks.payloadOperations=$operations.Count
  } else {
    Add-Warning 'PAYLOAD_NOT_PROVIDED' 'No compiled payload was provided; matrix dimensions were not checked.'
  }

  # Verify that the report contract itself serializes on both success and failure paths.
  [void]($report | ConvertTo-Json -Depth 12)
  $report.checks.reportSerialization=$true
  if($report.errors.Count -eq 0 -and (-not $FailOnWarning -or $report.warnings.Count -eq 0)){$report.state='PASS_OFFLINE_PREFLIGHT'}
}
catch {
  Add-Error 'PREFLIGHT_EXCEPTION' ($_.Exception.Message+' | '+$_.ScriptStackTrace)
}

$json=$report|ConvertTo-Json -Depth 12
$json
if($report.state -ne 'PASS_OFFLINE_PREFLIGHT'){exit 1}

# Compila las guias Markdown a PDF VISUALES (color, cajas) en Apuntes/pdf/visual/
# No modifica los PDF de Apuntes/pdf/
# Uso: .\compile-guias-visual.ps1

$ErrorActionPreference = "Continue"
$BuildDir = $PSScriptRoot
$ApuntesDir = Split-Path $BuildDir -Parent
$PdfDir = Join-Path $ApuntesDir "pdf\visual"

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

if (-not (Test-Command "pandoc")) {
    Write-Error "pandoc no encontrado. Instala con: winget install --id JohnMacFarlane.Pandoc -e"
    exit 1
}
if (-not (Test-Command "xelatex")) {
    Write-Error "xelatex no encontrado. Instala con: winget install --id MiKTeX.MiKTeX -e"
    exit 1
}

if (-not (Test-Path $PdfDir)) {
    New-Item -ItemType Directory -Path $PdfDir -Force | Out-Null
}

$guias = @(
    "Guia_Auditoria_Windows.md",
    "Guia_Certificados_Windows.md",
    "Guia_Examen_Criptografia.md",
    "Guia_Nmap.md",
    "Guia_SSL_Firewall.md",
    "Guia_Wireshark.md"
)

$metadata = Join-Path $BuildDir "metadata-visual.yaml"
$preamble = Join-Path $BuildDir "preamble-visual.tex"
$luaFilter = Join-Path $BuildDir "tip-boxes.lua"
$failed = @()
$ok = 0

Write-Host "Salida: pdf\visual\" -ForegroundColor Cyan
Write-Host ""

foreach ($md in $guias) {
    $input = Join-Path $ApuntesDir $md
    $base = [System.IO.Path]::GetFileNameWithoutExtension($md)
    $output = Join-Path $PdfDir "$base.pdf"

    if (-not (Test-Path $input)) {
        Write-Host "[SKIP] $md - archivo no encontrado" -ForegroundColor Yellow
        $failed += $md
        continue
    }

    Write-Host "Compilando $md -> pdf\visual\$base.pdf ..." -NoNewline

    $args = @(
        $input,
        "-o", $output,
        "--from=markdown",
        "--pdf-engine=xelatex",
        "--metadata-file=$metadata",
        "-H", $preamble,
        "--lua-filter=$luaFilter",
        "--highlight-style=kate",
        "-V", "linkcolor:blue"
    )

    $null = & pandoc @args 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host " ERROR" -ForegroundColor Red
        & pandoc @args 2>&1
        $failed += $md
    } else {
        Write-Host " OK" -ForegroundColor Green
        $ok++
    }
}

Write-Host ""
Write-Host "Resumen visual: $ok correctos, $($failed.Count) fallidos"
if ($failed.Count -gt 0) {
    Write-Host "Fallidos: $($failed -join ', ')" -ForegroundColor Red
    exit 1
}

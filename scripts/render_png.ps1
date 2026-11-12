param(
    [Parameter(Mandatory = $true)][string]$Pptx,
    [Parameter(Mandatory = $true)][string]$OutDir
)
# PowerPoint COM 으로 모든 슬라이드를 PNG(1600x900)로 내보낸다.
# 슬라이드 1장: <basename>.png / 여러 장: NN.png
$ErrorActionPreference = "Stop"
$Pptx = (Resolve-Path $Pptx).Path
New-Item -ItemType Directory -Force $OutDir | Out-Null
$OutDir = (Resolve-Path $OutDir).Path
$base = [System.IO.Path]::GetFileNameWithoutExtension($Pptx)
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($Pptx, $true, $false, $false)
    $n = $pres.Slides.Count
    for ($i = 1; $i -le $n; $i++) {
        if ($n -eq 1) { $name = "$base.png" } else { $name = ("{0:D2}.png" -f $i) }
        $pres.Slides.Item($i).Export((Join-Path $OutDir $name), "PNG", 1600, 900)
    }
    $pres.Close()
    Write-Output "exported $n slide(s) to $OutDir"
} finally {
    $app.Quit()
}

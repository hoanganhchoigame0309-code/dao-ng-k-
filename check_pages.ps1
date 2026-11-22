$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Resolve-Path "FOX_LAB_BAO_CAO_KHKT_CHINH_THUC.docx").Path
$doc = $word.Documents.Open($docPath)
$pages = $doc.ComputeStatistics(2)
Write-Host "EXACT_PAGES: $pages"
$doc.Close([ref]$false)
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null

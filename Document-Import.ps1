<#--------------------------------------------------------------------------------------------------------------
Description: The script is used to import document list to IT asset
Author: Tom
Date: 2022-10-14
----------------------------------------------------------------------------------------------------------------#>

#Define
$myKey = "V3GBGv5K"
#$DocumentPath = @("\\kunsw19file1\it$\00. IT_Process And Policy","\\kunsw19file1\it$\02. Network","\\kunsw19file1\it$\03. IT_Routine And Review","\\kunsw19file1\it$\04. SOX","\\kunsw19file1\it$\11. Security Control Project")
$DocumentPath = @("F:\IT\04. SOX")
$Filters = @('*.doc*','*.xls*','*.ppt*','*.pdf')

###Clean all document list in database
#Invoke-RestMethod -Method Post -Body @{myKey = $myKey} -Uri "http://kunsw16test1.snaponglobal.com:8080/document/api/documentClean"


###Upload document list to database

foreach ($Filter in $Filters)
    {
    $Documents = Get-ChildItem $DocumentPath -Filter $Filter -Recurse |Select-Object name,DirectoryName,LastWriteTime,LastAccessTime
    foreach ($Document in $Documents)
        {
            $folder_path = $Document.DirectoryName -replace 'F:\\IT','\\kunsw19file1\it$'
            $body = @{
                myKey = $myKey
                name = "{0}" -f $Document.name
                folder = $folder_path
                lastwrite = ($Document.LastWriteTime).ToString("yyyy-MM-dd HH:mm:ss")
                }
            #$body
            # Invoke-RestMethod -Body $body -Method Post -Uri "http://kunsw16test1.snaponglobal.com:8080/document/api/documentImport"
            $body
        }
    }





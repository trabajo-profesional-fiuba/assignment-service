Param(
    [switch]
    [Parameter(HelpMessage = "Use this switch to start the database.")]
    $StartDatabase
)


function StartDatabaseIfNeeded($StartDatabase) {
    if ($StartDatabase) {
        $Containers = docker ps --filter "name=postgres"
        if ($Containers.Length -eq 2) {
            Write-Host "Dropping current database container"
            .\InitTestDatabase.ps1 -StopDatabase
            Start-Sleep -Seconds 5
        }
        Write-Host "Starting database"
        .\InitTestDatabase.ps1
        Start-Sleep -Seconds 5
    }    
}

function CheckPythonInterpreter {
    $Interpreter = Get-Command python | Select-Object -Property Source
    if ($Interpreter.Source -match "virtualenvs") {
        return $true
    }

    $false
}

function Main ($StartDatabase) {

    if (CheckPythonInterpreter) {
        StartDatabaseIfNeeded($StartDatabase)

        Write-Host -ForegroundColor Green "Running Alembic migrations"
        alembic upgrade head

        Write-Host -ForegroundColor Green "Starting python app"
        python .\main.py

    }
    else {
        Write-Host -ForegroundColor Blue "To execute this script, the python interpreter should be the one inside poetry enviroment"
    }
}

Main $StartDatabase
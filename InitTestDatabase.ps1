Param(
    [switch]
    $StopDatabase,

    [switch]
    $ApplyMigrations
)

function IsDockerInstalledAndRunning() {
    if (Get-Command docker) {
        Write-Host "Docker installed: "-NoNewline; Write-Host -ForegroundColor Green "Yes"
        $info = docker info 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Docker is running."
            return $true
        }
        else {
            Write-Host "Docker is not running. Please start the engine."
            return $false
        }
    }


    Write-Host "Docker installed: "-NoNewline; Write-Host -ForegroundColor Red "No"
    Write-Host "Please install docker from: https://www.docker.com/"
    
    return $false
}
function PythonInterpreterInVirtualEnv {
    $Interpreter = Get-Command python | Select-Object -Property Source
    if ($Interpreter.Source -match "virtualenvs") {
        return $true
    }

    $false
}


if (IsDockerInstalledAndRunning) {
    if (!$StopDatabase) {
        Write-Host "Starting PostgreSQL 15 container..."
    
        docker run -d --rm `
            -e POSTGRES_USER=postgres `
            -e POSTGRES_PASSWORD=postgres `
            -e POSTGRES_DB=postgres `
            -p 5433:5432 `
            --name postgres `
            postgres:15
    
        $postgresUrl = "postgres://postgres:postgres@localhost:5433/postgres"
    
        Write-Host "PostgreSQL container started."
        Write-Host -ForegroundColor Yellow "Container information"
        docker ps
    
        Write-Host -ForegroundColor Cyan "URL Connection: $postgresUrl"

        if ($ApplyMigrations) {
            Write-Host "Applying migrations to the database"
            Start-Sleep -Seconds 3
            if (PythonInterpreterInVirtualEnv){
                Invoke-Expression -Command "alembic upgrade head"
            }
            else {
                Invoke-Expression -Command "poetry alembic upgrade head"
            }
        }
    }
    else {
        Write-Host "Stopping and removing PostgreSQL 15 container..."
        $_ = docker stop postgres 2>$null
        docker ps
    }
    
}


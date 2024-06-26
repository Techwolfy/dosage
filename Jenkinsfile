def pys = [
    [name: 'Python 3.10', docker: 'python:3.10-bullseye', tox:'py310,flake8', main: true],
    [name: 'Python 3.9',  docker: 'python:3.9-bullseye',  tox:'py39', main: false],
    [name: 'Python 3.8',  docker: 'python:3.8-bullseye',  tox:'py38', main: false],
    [name: 'Python 3.7',  docker: 'python:3.7-bullseye',  tox:'py37', main: false],
]

properties([
    durabilityHint('PERFORMANCE_OPTIMIZED'),
    buildDiscarder(logRotator(numToKeepStr: '100')),
])

Map tasks = [failFast: true]

pys.each { py ->
    tasks[py.name] = {
        node {
            stage("Checkout $py.name") {
                checkout scm
                sh '''
                    git clean -fdx
                    git fetch --tags
                '''
            }

            stage("Build $py.name") {
                def image = docker.image(py.docker)
                image.pull()
                image.inside {
                    withEnv(['HOME=' + pwd(tmp: true)]) {
                        warnError('tox failed') {
                            sh """
                                pip install --no-warn-script-location tox
                                python -m tox -e $py.tox
                            """
                        }

                        if (py.main) {
                            sh """
                                pip install --no-warn-script-location build
                                python -m build
                            """
                        }
                    }
                }

                if (py.main) {
                    archiveArtifacts artifacts: 'dist/*', fingerprint: true
                    stash includes: 'dist/*.tar.gz', name: 'bin'
                    dir('.tox/reports') {
                        stash includes: '*/allure-data/**', name: 'allure-data'
                    }
                    def buildVer = findFiles(glob: 'dist/*.tar.gz')[0].name.replaceFirst(/\.tar\.gz$/, '')
                    currentBuild.description = buildVer

                    publishCoverage calculateDiffForChangeRequests: true,
                        sourceFileResolver: sourceFiles('STORE_LAST_BUILD'),
                        adapters: [
                            coberturaAdapter('.tox/reports/*/coverage.xml')
                        ]

                    recordIssues sourceCodeEncoding: 'UTF-8',
                        referenceJobName: 'dosage/master',
                        tool: flake8(pattern: '.tox/flake8.log', reportEncoding: 'UTF-8')
                }
                junit '.tox/reports/*/junit.xml'
            }
        }
    }
}

// MAIN //

parallel(tasks)
stage('Windows binary') {
    windowsBuild()
}
stage('Allure report') {
    processAllure()
}

def windowsBuild() {
    warnError('windows build failed') {
        node {
            windowsBuildCommands()
        }
    }
}

def windowsBuildCommands() {
    deleteDir()
    unstash 'bin'
    // Keep 3.8 for now, so we are still compatible with Windows 7
    def img = docker.image('tobix/pywine:3.8')
    img.pull()
    img.inside {
        sh '''
            . /opt/mkuserwineprefix
            tar xvf dist/dosage-*.tar.gz
            cd dosage-*
            xvfb-run sh -c "
                wine py -m pip install -e .[css] &&
                cd scripts &&
                wine py -m PyInstaller -y dosage.spec;
                wineserver -w" 2>&1 | tee log.txt
        '''
        archiveArtifacts '*/scripts/dist/*'
    }
}

def processAllure() {
    warnError('allure report failed') {
        node {
            deleteDir()
            unstash 'allure-data'
            sh 'mv */allure-data .'
            copyArtifacts filter: 'allure-history.zip', optional: true, projectName: JOB_NAME, selector: lastWithArtifacts()
            if (fileExists('allure-history.zip')) {
                unzip dir: 'allure-data', quiet: true, zipFile: 'allure-history.zip'
                sh 'rm -f allure-history.zip'
            }
            sh 'docker run --rm -v $PWD:/work -u $(id -u) tobix/allure-cli generate allure-data'
            zip archive: true, dir: 'allure-report', glob: 'history/**', zipFile: 'allure-history.zip'
            publishHTML reportDir: 'allure-report', reportFiles: 'index.html', reportName: 'Allure Report'
        }
    }
}

// vim: set ft=groovy:

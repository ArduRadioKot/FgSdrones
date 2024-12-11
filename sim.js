class SimpleEditor {
            constructor(textarea) {
                this.textarea = textarea;
                this.textarea.style.display = 'none';
                this.editor = document.createElement('div');
                this.editor.contentEditable = true;
                this.editor.style.width = '100%';
                this.editor.style.height = '100%';
                this.editor.style.backgroundColor = '#1a252f';
                this.editor.style.color = 'white';
                this.editor.style.fontFamily = 'Courier New, Courier, monospace';
                this.editor.style.fontSize = '16px';
                this.editor.style.padding = '20px';
                this.editor.style.boxSizing = 'border-box';
                this.editor.innerText = this.textarea.value;
                this.textarea.parentNode.insertBefore(this.editor, this.textarea.nextSibling);
            }

            getValue() {
                return this.editor.innerText;
            }

            setValue(value) {
                this.editor.innerText = value;
            }
        }

        var editor = new SimpleEditor(document.getElementById("code"));
        var mobileEditor = new SimpleEditor(document.getElementById("mobile-code"));

        var robot = document.getElementById("robot");
        var mobileRobot = document.getElementById("mobile-robot");
        var gridSize = 100; // Size of each grid cell in pixels
        var position = { x: 0, y: 0 };
        var mobilePosition = { x: 0, y: 0 };

        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        async function runCode() {
            var code = editor.getValue();
            var commands = code.split('\n');
            for (var command of commands) {
                if (command.startsWith('forward(')) {
                    var steps = parseInt(command.match(/\d+/)[0]);
                    for (var i = 0; i < steps; i++) {
                        position.y -= gridSize;
                        robot.style.transform = `translate(${position.x}px, ${position.y}px)`;
                        await sleep(500);
                    }
                } else if (command.startsWith('back(')) {
                    var steps = parseInt(command.match(/\d+/)[0]);
                    for (var i = 0; i < steps; i++) {
                        position.y += gridSize;
                        robot.style.transform = `translate(${position.x}px, ${position.y}px)`;
                        await sleep(500);
                    }
                } else if (command.startsWith('start(')) {
                    position = { x: 0, y: 0 };
                    robot.style.transform = `translate(${position.x}px, ${position.y}px)`;
                    await sleep(500);
                } else if (command.startsWith('landing(')) {
                    // Add landing logic if needed
                }
            }
        }

        async function runMobileCode() {
            var code = mobileEditor.getValue();
            var commands = code.split('\n');
            for (var command of commands) {
                if (command.startsWith('forward(')) {
                    var steps = parseInt(command.match(/\d+/)[0]);
                    for (var i = 0; i < steps; i++) {
                        mobilePosition.y -= gridSize;
                        mobileRobot.style.transform = `translate(${mobilePosition.x}px, ${mobilePosition.y}px)`;
                        await sleep(500);
                    }
                } else if (command.startsWith('back(')) {
                    var steps = parseInt(command.match(/\d+/)[0]);
                    for (var i = 0; i < steps; i++) {
                        mobilePosition.y += gridSize;
                        mobileRobot.style.transform = `translate(${mobilePosition.x}px, ${mobilePosition.y}px)`;
                        await sleep(500);
                    }
                } else if (command.startsWith('start(')) {
                    mobilePosition = { x: 0, y: 0 };
                    mobileRobot.style.transform = `translate(${mobilePosition.x}px, ${mobilePosition.y}px)`;
                    await sleep(500);
                } else if (command.startsWith('landing(')) {
                    // Add landing logic if needed
                }
            }
        }

        function saveCode() {
            var code = editor.getValue();
            localStorage.setItem('savedCode', code);
            alert('Code saved!');
        }

        function deleteCode() {
            localStorage.removeItem('savedCode');
            editor.setValue('');
            alert('Code deleted!');
        }

        function openCode() {
            var input = document.createElement('input');
            input.type = 'file';
            input.accept = '.txt,.js';
            input.onchange = function(event) {
                var file = event.target.files[0];
                if (file) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        editor.setValue(e.target.result);
                    };
                    reader.readAsText(file);
                }
            };
            input.click();
        }

        function showHelp() {
            alert('Help: \n\n- Use start(); to initialize the drone.\n- Use forward(n); to move the drone forward by n cells.\n- Use back(n); to move the drone backward by n cells.\n- Use landing(); to land the drone.');
        }

        function showCodeEditor() {
            document.querySelector('.code-editor').style.display = 'block';
            document.querySelector('.grid').style.display = 'none';
        }

        function showGrid() {
            document.querySelector('.code-editor').style.display = 'none';
            document.querySelector('.grid').style.display = 'grid';
        }

        window.onload = function() {
            var savedCode = localStorage.getItem('savedCode');
            if (savedCode) {
                editor.setValue(savedCode);
            }

        }
        function goToAnotherPage() {
            window.location.href = 'index.html'; // Замените 'anotherPage.html' на нужный вам файл
        }

import os

html_content = r"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOOM 3D · МУЛЬТИПЛЕЕР И ЛОББИ</title>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Courier New', monospace; background: #000; color: #fff; }
        
        #startMenu {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle, rgba(60,20,20,1) 0%, rgba(0,0,0,1) 100%);
            display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 1000;
        }
        #mainMenu, #authPanel, #lobbyPanel {
            background: rgba(20,20,30,0.95); border: 3px solid #d97c2b; padding: 40px; border-radius: 15px; width: 380px;
            box-shadow: 0 0 40px #f90; text-align: center;
        }
        #authPanel, #lobbyPanel { display: none; }
        h1 { color: #f90; font-size: 72px; text-shadow: 0 0 40px #f90; margin-bottom: 20px; font-weight: 900; letter-spacing: 5px; }
        h2 { color: #f90; margin-top: 0; font-size: 28px; }
        #lobbyPanel h2 { color: #0f0; text-shadow: 0 0 20px #0f0; }
        
        #authError { color: #ff4d4d; margin-bottom: 10px; font-weight: bold; }
        input[type="text"], input[type="password"] { 
            width: 100%; margin-bottom: 15px; padding: 10px; box-sizing: border-box; background: #111; 
            border: 1px solid #f90; color: #fff; border-radius: 5px; font-size: 16px;
        }
        .authBtn { 
            width: 100%; padding: 12px; margin-bottom: 15px; background: #b55f2a; border: 2px solid #fd9; 
            color: #fff; font-weight: bold; cursor: pointer; transition: 0.2s; border-radius: 5px; font-size: 16px;
        }
        .authBtn:hover { background: #d97c2b; box-shadow: 0 0 20px #f90; }
        .backBtn { background: #444 !important; border-color: #888 !important; }
        #gameUI { display: none; }

        #info {
            position: absolute; top: 20px; left: 20px; background: rgba(0,0,0,0.9); padding: 12px 24px;
            border-left: 6px solid #f70; z-index: 100; font-size: 22px; border-radius: 0 12px 12px 0;
            box-shadow: 0 0 20px rgba(255,100,0,0.3);
        }
        #ammo { color: #ffb347; text-shadow: 0 0 10px #ff9900; }
        #health { color: #ff4d4d; text-shadow: 0 0 10px #ff0000; }
        #playersOnline { color: #7fffd4; margin-left: 15px; text-shadow: 0 0 10px #00ffff; }
        #crosshair {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            font-size: 48px; color: #ff0000; z-index: 50; pointer-events: none;
            text-shadow: 0 0 20px #ff0000; transition: all 0.2s;
        }
        
        #menuPanel {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(20,20,30,0.98);
            border: 4px solid #f90; padding: 30px; width: 400px; z-index: 3000;
            border-radius: 20px; box-shadow: 0 0 100px #f90; backdrop-filter: blur(15px);
            display: none;
        }
        #menuPanel h3 { margin: 0 0 20px; color: #f90; text-align: center; font-size: 28px; }
        
        #playerListBox {
            background: #111; padding: 15px; border-radius: 8px; border: 1px solid #444;
            max-height: 120px; overflow-y: auto; margin-bottom: 20px; text-align: left;
        }
        .player-item { color: #0f0; margin-bottom: 5px; font-weight: bold; }
        #status { position: absolute; top: 20px; right: 20px; background: rgba(0,0,0,0.9); padding: 12px 24px; border: 2px solid #0f0; color: #0f0; z-index: 100; border-radius: 30px; font-size: 18px; box-shadow: 0 0 20px #0f0; }
        #fps-counter { position: absolute; top: 20px; right: 300px; background: rgba(0,0,0,0.7); padding: 8px 15px; border-radius: 20px; color: #0f0; font-size: 18px; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <div id="startMenu">
        <h1>DOOM 3D</h1>
        
        <div id="mainMenu">
            <button class="authBtn" id="btnShowAuth">ИГРАТЬ ПО СЕТИ</button>
            <button class="authBtn" id="openSettingsBtn_Global">НАСТРОЙКИ</button>
        </div>

        <div id="authPanel">
            <h2>АВТОРИЗАЦИЯ</h2>
            <div id="authError"></div>
            <input type="text" id="usernameInput" placeholder="Имя пользователя">
            <input type="password" id="passwordInput" placeholder="Пароль">
            <button class="authBtn" id="loginBtn">ВОЙТИ</button>
            <button class="authBtn" id="registerBtn">РЕГИСТРАЦИЯ</button>
            <button class="authBtn backBtn" onclick="showMainMenu()">⬅ НАЗАД</button>
        </div>

        <div id="lobbyPanel">
            <h2>ЛОББИ КОМНАТЫ</h2>
            <div id="playerListBox">
                <div style="color: #666; font-size: 12px; margin-bottom: 8px;">КТО В ЛОББИ:</div>
                <div id="connectedPlayersList">Подключение...</div>
            </div>
            <p style="color: #aaa; font-size: 14px; margin-bottom: 10px;">Пригласи друга:</p>
            <div style="background: #000; padding: 12px; border: 1px dashed #f90; border-radius: 5px; color: #f90; margin-bottom: 20px; font-size: 13px; word-break: break-all;" id="inviteLink"></div>
            <button class="authBtn" id="copyLinkBtn">📄 СКОПИРОВАТЬ ССЫЛКУ</button>
            <button class="authBtn" id="startGameBtn" style="background: #0a0; border-color: #0f0; font-size: 20px;">🎮 ЗАЙТИ В АРЕНУ</button>
            <button class="authBtn backBtn" onclick="window.location.reload()">🚪 ВЫЙТИ</button>
        </div>
    </div>

    <div id="gameUI">
        <div id="info">❤️ <span id="health">150</span> 🔫 <span id="ammo">30/30</span> 👥 <span id="playersOnline">1</span>/8</div>
        <div id="fps-counter">FPS: <span id="fpsValue">60</span></div>
        <div id="status">🔄 ПОИСК СИГНАЛА...</div>
        <div id="crosshair">+</div>
    </div>
    
    <div id="menuPanel">
        <button id="closeSettingsBtn" style="position: absolute; top: 15px; right: 15px; background: #a55; border: none; color: #fff; cursor: pointer; border-radius: 5px; padding: 5px 15px; font-weight: bold;">X</button>
        <h3>⚡ НАСТРОЙКИ ⚡</h3>
        <div style="padding: 10px; background: rgba(0,0,0,0.5); border-radius: 10px;">
            <label style="color: #f90;">ЧУВСТВИТЕЛЬНОСТЬ: <span id="sensVal">2.0</span></label><br>
            <input type="range" id="mouseSens" min="0.5" max="5.0" value="2.0" step="0.1" style="width: 100%;"><br><br>
            <button id="quitGameBtn" style="background: #a00; color: #fff; border: none; padding: 10px; width: 100%; border-radius: 5px; cursor: pointer;">🛑 ВЫЙТИ ИЗ ИГРЫ</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.photonengine.com/api/sdk/4.1.12.1/photon-sdk.min.js"></script>

    <script>
    const API_URL = window.location.origin;
    const APP_ID = 'e8e01bce-e246-44a2-ab26-9f09c5704b7d';
    let myUsername = '', targetRoomID = '', gameStarted = false, photon = null;

    const urlParams = new URLSearchParams(window.location.search);
    targetRoomID = urlParams.get('room') || 'ARENA_' + Math.random().toString(36).substring(2, 7).toUpperCase();

    function showMainMenu() {
        document.getElementById('mainMenu').style.display = 'block';
        document.getElementById('authPanel').style.display = 'none';
        document.getElementById('authError').innerText = '';
    }

    document.getElementById('btnShowAuth').addEventListener('click', () => {
        document.getElementById('mainMenu').style.display = 'none';
        document.getElementById('authPanel').style.display = 'block';
    });

    async function handleAuth(endpoint) {
        const uInput = document.getElementById('usernameInput');
        const pInput = document.getElementById('passwordInput');
        const authError = document.getElementById('authError');
        if(!uInput.value || !pInput.value) { authError.innerText = 'Заполните поля'; return; }
        
        try {
            const res = await fetch(API_URL + endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: uInput.value, password: pInput.value })
            });
            const data = await res.json();
            if(!res.ok) { 
                authError.innerText = data.error || 'Ошибка';
            } else { 
                myUsername = data.username || uInput.value;
                showLobby();
            }
        } catch(e) {
            authError.innerText = 'Сервер недоступен!';
        }
    }

    document.getElementById('loginBtn').addEventListener('click', () => handleAuth('/login'));
    document.getElementById('registerBtn').addEventListener('click', () => handleAuth('/register'));
    document.getElementById('openSettingsBtn_Global').addEventListener('click', () => { document.getElementById('menuPanel').style.display = 'block'; });
    document.getElementById('closeSettingsBtn').addEventListener('click', () => { document.getElementById('menuPanel').style.display = 'none'; });
    document.getElementById('quitGameBtn').addEventListener('click', () => { window.location.reload(); });

    function showLobby() {
        document.getElementById('authPanel').style.display = 'none';
        document.getElementById('lobbyPanel').style.display = 'block';
        document.getElementById('inviteLink').innerText = window.location.origin + window.location.pathname + "?room=" + targetRoomID;
        initMultiplayer(); // Подключаемся к Photon СРАЗУ в лобби
    }

    document.getElementById('copyLinkBtn').addEventListener('click', () => {
        navigator.clipboard.writeText(document.getElementById('inviteLink').innerText).then(() => {
            document.getElementById('copyLinkBtn').innerText = '✅ СКОПИРОВАНО!';
            setTimeout(() => { document.getElementById('copyLinkBtn').innerText = '📄 СКОПИРОВАТЬ ССЫЛКУ'; }, 2000);
        });
    });

    document.getElementById('startGameBtn').addEventListener('click', () => {
        if(photon && photon.myRoom()) {
            startGame();
        } else {
            alert('Сначала дождитесь подключения к серверу!');
        }
    });

    function initMultiplayer() {
        photon = new Photon.LoadBalancing.LoadBalancingClient(Photon.ConnectionProtocol.Wss, APP_ID, '1.0');
        photon.connectToRegion('eu');
        photon.addEventListener(Photon.LoadBalancing.EventName.CONNECTED_TO_MASTER, () => {
            photon.myActor().setName(myUsername);
            photon.opJoinOrCreateRoom(targetRoomID);
        });
        photon.addEventListener(Photon.LoadBalancing.EventName.JOINED_ROOM, () => {
            updatePlayerListUI();
        });
        photon.addEventListener(Photon.LoadBalancing.EventName.ACTOR_JOINED, updatePlayerListUI);
        photon.addEventListener(Photon.LoadBalancing.EventName.ACTOR_LEFT, (act) => {
            if(otherPlayers.has(act.actorNr)) { scene.remove(otherPlayers.get(act.actorNr)); otherPlayers.delete(act.actorNr); }
            updatePlayerListUI();
        });
        photon.addEventListener(Photon.LoadBalancing.EventName.RAISE_EVENT, (code, data, actorNr) => {
            if(code === 1 && gameStarted) {
                if(!otherPlayers.has(actorNr)) {
                    const op = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.4, 1.2), new THREE.MeshStandardMaterial({ color: 0x00aaff }));
                    scene.add(op); otherPlayers.set(actorNr, op);
                }
                const p = otherPlayers.get(actorNr);
                p.position.set(data.x, data.y, data.z); p.rotation.y = data.ry;
            }
        });
    }

    function updatePlayerListUI() {
        const listDiv = document.getElementById('connectedPlayersList');
        const cOnline = document.getElementById('playersOnline');
        if(!photon || !photon.myRoom()) return;
        
        let names = [];
        photon.actors.getAll().forEach(act => names.push('<div class="player-item">👤 ' + (act.name || "Гость") + '</div>'));
        listDiv.innerHTML = names.join('');
        cOnline.innerText = photon.actors.count;
        document.getElementById('status').innerText = '🟢 СЕРВЕР: ' + targetRoomID;
    }

    // Three.js Game Logic
    let scene, camera, renderer, weaponGroup;
    let otherPlayers = new Map();
    let bullets = [], enemies = [], keys = {}, yaw = 0, pitch = 0, health = 150, ammo = 30;
    let settings = { mouseSens: 2.0 };

    function startGame() {
        document.getElementById('startMenu').style.display = 'none';
        document.getElementById('gameUI').style.display = 'block';
        gameStarted = true;
        initScene();
        animate();
        renderer.domElement.requestPointerLock();
    }

    function initScene() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0a);
        scene.fog = new THREE.Fog(0x0a0a0a, 5, 60);

        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 2, 0);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const dl = new THREE.DirectionalLight(0xff0000, 0.5); dl.position.set(5, 10, 5); scene.add(dl);

        const floor = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), new THREE.MeshStandardMaterial({ color: 0x111111 }));
        floor.rotation.x = -Math.PI / 2; scene.add(floor);
        scene.add(new THREE.GridHelper(100, 40, 0x440000, 0x222222));

        weaponGroup = new THREE.Group();
        const pBody = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.4, 0.8), new THREE.MeshStandardMaterial({ color: 0x111 }));
        pBody.position.set(0.5, -0.4, -0.8); weaponGroup.add(pBody);
        camera.add(weaponGroup); scene.add(camera);

        for(let i=0; i<15; i++) {
            const e = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2.5, 1.5), new THREE.MeshStandardMaterial({ color: 0xaa0000 }));
            e.position.set((Math.random()-0.5)*70, 1.25, (Math.random()-0.5)*70);
            scene.add(e); enemies.push({ mesh: e, alive: true });
        }
    }

    function animate() {
        if(!gameStarted) return;
        requestAnimationFrame(animate);
        if(document.pointerLockElement) {
            const move = new THREE.Vector3();
            if(keys['KeyW']) move.z -= 1; if(keys['KeyS']) move.z += 1;
            if(keys['KeyA']) move.x -= 1; if(keys['KeyD']) move.x += 1;
            move.applyQuaternion(camera.quaternion); move.y = 0;
            camera.position.add(move.normalize().multiplyScalar(0.15));
            if(photon && photon.myRoom()) photon.raiseEvent(1, { x: camera.position.x, y: camera.position.y, z: camera.position.z, ry: camera.rotation.y });
        }
        renderer.render(scene, camera);
    }

    window.addEventListener('keydown', e => keys[e.code] = true);
    window.addEventListener('keyup', e => keys[e.code] = false);
    window.addEventListener('mousemove', e => {
        if(document.pointerLockElement) {
            yaw -= e.movementX * 0.002 * settings.mouseSens;
            pitch = Math.max(-1.4, Math.min(1.4, pitch - e.movementY * 0.002 * settings.mouseSens));
            camera.rotation.set(pitch, yaw, 0, 'YXZ');
        }
    });

    document.getElementById('mouseSens').addEventListener('input', e => {
        settings.mouseSens = parseFloat(e.target.value);
        document.getElementById('sensVal').innerText = settings.mouseSens.toFixed(1);
    });

    window.addEventListener('resize', () => {
        if(!renderer) return;
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    </script>
</body>
</html>
"""

with open("c:/Users/Sasha/Downloads/fix11/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

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
            background: rgba(20,20,30,0.95); border: 3px solid #d97c2b; padding: 40px; border-radius: 15px; width: 350px;
            box-shadow: 0 0 40px #f90; text-align: center;
        }
        #authPanel, #lobbyPanel { display: none; }
        h1 { color: #f90; font-size: 72px; text-shadow: 0 0 40px #f90; margin-bottom: 40px; font-weight: 900; letter-spacing: 5px; }
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
        #openSettingsBtn { background: #444; border-color: #888; }
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
        
        .menu-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #f90; padding-bottom: 10px; }
        .menu-tab { flex: 1; text-align: center; padding: 10px; cursor: pointer; color: #ca9; border-radius: 8px 8px 0 0; transition: all 0.2s; font-weight: bold; }
        .menu-tab.active { color: #f90; background: rgba(255,150,0,0.1); border-bottom: 3px solid #f90; }
        .menu-section { display: none; }
        .menu-section.active { display: block; }
        
        .setting-item { margin-bottom: 15px; padding: 12px; background: rgba(0,0,0,0.5); border-radius: 10px; border: 1px solid #333; }
        .setting-item label { display: block; color: #ffaa00; margin-bottom: 8px; font-size: 16px; font-weight: bold; }
        .setting-item input[type=range] { width: 100%; height: 8px; background: #333; border-radius: 4px; -webkit-appearance: none; accent-color: #f90; }
        .setting-item input[type=color] { width: 100%; height: 40px; border: 2px solid #f90; border-radius: 8px; background: transparent; cursor: pointer; }
        .setting-item select { width: 100%; padding: 10px; background: #2a1f15; color: #ca9; border: 2px solid #a55; border-radius: 8px; font-size: 16px; }
        .value-display { float: right; color: #7fffd4; font-weight: bold; font-family: monospace; }
        
        .weapon-selector { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
        .weapon-btn { background: #2a1f15; color: #ca9; border: 2px solid #a55; padding: 12px; cursor: pointer; font-size: 16px; flex: 1 0 45%; border-radius: 8px; transition: all 0.2s; text-align: center; }
        .weapon-btn:hover { background: #b55f2a; color: #fff; border-color: #fd9; }
        .weapon-btn.active { background: #b55f2a; color: #fff; border-color: #fd9; box-shadow: 0 0 20px #f90; }
        
        #status { position: absolute; top: 20px; right: 20px; background: rgba(0,0,0,0.9); padding: 12px 24px; border: 2px solid #0f0; color: #0f0; z-index: 100; border-radius: 30px; font-size: 18px; box-shadow: 0 0 20px #0f0; }
        .instruction { position: absolute; bottom: 20px; left: 20px; background: rgba(0,0,0,0.8); padding: 15px 25px; color: #ffaa00; z-index: 100; border-radius: 30px; border-left: 6px solid #f70; font-size: 18px; box-shadow: 0 0 20px rgba(255,150,0,0.3); }
        #fps-counter { position: absolute; top: 20px; right: 300px; background: rgba(0,0,0,0.7); padding: 8px 15px; border-radius: 20px; color: #0f0; font-size: 18px; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <div id="startMenu">
        <h1>DOOM 3D</h1>
        
        <div id="mainMenu">
            <button class="authBtn" id="btnShowAuth">ИГРАТЬ ПО СЕТИ</button>
            <button class="authBtn" id="openSettingsBtn">НАСТРОЙКИ</button>
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
            <h2>ЛОББИ СЕРВЕРА</h2>
            <p style="color: #fff; font-size: 16px; margin-bottom: 20px;">Поделись ссылкой с другом:</p>
            <div style="background: #111; padding: 15px; border: 2px dashed #f90; border-radius: 10px; color: #ffaa00; margin-bottom: 25px; font-size: 14px; word-break: break-all;" id="inviteLink"></div>
            <button class="authBtn" id="copyLinkBtn">📄 СКОПИРОВАТЬ ССЫЛКУ</button>
            <button class="authBtn" id="startGameBtn" style="background: #0a0; border-color: #0f0; margin-top: 20px;">🎮 ПРИСОЕДИНИТЬСЯ В АРЕНУ</button>
            <button class="authBtn backBtn" onclick="window.location.reload()">🚪 ВЫЙТИ ИЗ ЛОББИ</button>
        </div>
    </div>

    <div id="gameUI">
        <div id="info">❤️ <span id="health">150</span> 🔫 <span id="ammo">30/30</span> 👥 <span id="playersOnline">1</span>/8</div>
        <div id="fps-counter">FPS: <span id="fpsValue">60</span></div>
        <div id="status">🔄 ОЖИДАНИЕ...</div>
        <div id="crosshair">+</div>
        <div class="instruction">ESC — Меню настроек | WASD — Ходьба | ЛКМ — Огонь | R — Перезарядка</div>
    </div>
    
    <div id="menuPanel">
        <button id="closeSettingsBtn" style="position: absolute; top: 15px; right: 15px; background: #a55; border: none; color: #fff; cursor: pointer; border-radius: 5px; padding: 5px 15px; font-weight: bold;">X</button>
        <h3>⚡ НАСТРОЙКИ ⚡</h3>
        
        <div class="menu-tabs">
            <div class="menu-tab active" data-tab="weapons">ОРУЖИЕ</div>
            <div class="menu-tab" data-tab="aim">ПРИЦЕЛ</div>
            <div class="menu-tab" data-tab="game">ИГРА</div>
        </div>
        
        <div class="menu-section active" id="tab-weapons">
            <div class="weapon-selector">
                <button class="weapon-btn active" id="wpPistol">🔫 ПИСТОЛЕТ</button>
                <button class="weapon-btn" id="wpShotgun">🔫🔫 ДРОБОВИК</button>
                <button class="weapon-btn" id="wpRifle">⚡ ВИНТОВКА</button>
                <button class="weapon-btn" id="wpRocket">💥 РОКЕТНИЦА</button>
            </div>
            <div style="margin-top: 20px; color: #ffaa00; font-size: 18px; text-align: left;">
                👾 ВРАГОВ НА КАРТЕ: <span id="enemyCount" class="value-display" style="float:none; margin-left:10px;">12</span><br>
                🟢 ИГРОКОВ ОНЛАЙН: <span id="onlineCount" class="value-display" style="float:none; margin-left:10px;">1</span>/8
            </div>
        </div>
        
        <div class="menu-section" id="tab-aim">
            <div class="setting-item">
                <label>ФОРМА ПРИЦЕЛА <span class="value-display" id="crosshairStyleVal">Плюс</span></label>
                <select id="crosshairStyle"><option value="plus" selected>➕ Плюс</option><option value="dot">• Точка</option><option value="circle">○ Круг</option><option value="cross">✖ Крест</option></select>
            </div>
            <div class="setting-item"><label>ЦВЕТ ПРИЦЕЛА</label><input type="color" id="crosshairColor" value="#ff0000"></div>
            <div class="setting-item"><label>РАЗМЕР <span class="value-display" id="crosshairSizeVal">48</span></label><input type="range" id="crosshairSize" min="24" max="72" value="48" step="2"></div>
            <div class="setting-item"><label>ЯРКОСТЬ <span class="value-display" id="crosshairOpacityVal">100%</span></label><input type="range" id="crosshairOpacity" min="0.3" max="1" value="1" step="0.1"></div>
        </div>
        
        <div class="menu-section" id="tab-game">
            <div class="setting-item"><label>ЧУВСТВИТЕЛЬНОСТЬ <span class="value-display" id="sensVal">2.0</span></label><input type="range" id="mouseSens" min="0.5" max="5.0" value="2.0" step="0.1"></div>
            <div class="setting-item"><label>СКОРОСТЬ <span class="value-display" id="speedVal">0.15</span></label><input type="range" id="moveSpeed" min="0.1" max="0.3" value="0.15" step="0.01"></div>
            <div class="setting-item"><label>ПРЫЖОК <span class="value-display" id="jumpVal">0.2</span></label><input type="range" id="jumpPower" min="0.1" max="0.4" value="0.2" step="0.01"></div>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <button id="quitGameBtn" style="background: #a00; color: #fff; border: 2px solid #f55; padding: 12px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%;">🛑 ВЫЙТИ ИЗ ИГРЫ</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.photonengine.com/api/sdk/4.1.12.1/photon-sdk.min.js"></script>

    <script>
    const API_URL = window.location.origin;
    let myUsername = '';
    let gameStarted = false;
    let targetRoomID = '';

    // Генерируем ID комнаты если нет в URL
    const urlParams = new URLSearchParams(window.location.search);
    const roomFromUrl = urlParams.get('room');
    targetRoomID = roomFromUrl || 'ARENA_' + Math.random().toString(36).substring(2, 7).toUpperCase();

    const authError = document.getElementById('authError');
    const uInput = document.getElementById('usernameInput');
    const pInput = document.getElementById('passwordInput');

    function showMainMenu() {
        document.getElementById('mainMenu').style.display = 'block';
        document.getElementById('authPanel').style.display = 'none';
        authError.innerText = '';
    }

    document.getElementById('btnShowAuth').addEventListener('click', () => {
        document.getElementById('mainMenu').style.display = 'none';
        document.getElementById('authPanel').style.display = 'block';
    });

    async function handleAuth(endpoint) {
        if(!uInput.value || !pInput.value) { authError.innerText = 'Заполните поля'; return; }
        authError.style.color = '#fff'; authError.innerText = 'Подключение...';
        try {
            const res = await fetch(API_URL + endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: uInput.value, password: pInput.value })
            });
            const data = await res.json();
            if(!res.ok) { 
                authError.innerText = data.error || 'Ошибка сервера';
                authError.style.color = '#ff4d4d';
            } else { 
                myUsername = data.username || uInput.value;
                if (roomFromUrl) {
                    startGame();
                } else {
                    showLobby();
                }
            }
        } catch(e) {
            authError.style.color = '#ff4d4d';
            authError.innerText = 'Сервер недоступен. Проверьте настройки на Render!';
        }
    }

    document.getElementById('loginBtn').addEventListener('click', () => handleAuth('/login'));
    document.getElementById('registerBtn').addEventListener('click', () => handleAuth('/register'));
    document.getElementById('openSettingsBtn').addEventListener('click', () => { document.getElementById('menuPanel').style.display = 'block'; });
    document.getElementById('closeSettingsBtn').addEventListener('click', () => { document.getElementById('menuPanel').style.display = 'none'; });
    document.getElementById('quitGameBtn').addEventListener('click', () => { window.location.reload(); });

    function showLobby() {
        document.getElementById('authPanel').style.display = 'none';
        document.getElementById('lobbyPanel').style.display = 'block';
        const link = window.location.origin + window.location.pathname + "?room=" + targetRoomID;
        document.getElementById('inviteLink').innerText = link;
    }

    document.getElementById('copyLinkBtn').addEventListener('click', () => {
        const link = document.getElementById('inviteLink').innerText;
        navigator.clipboard.writeText(link).then(() => {
            const btn = document.getElementById('copyLinkBtn');
            btn.innerText = '✅ СКОПИРОВАНО!';
            setTimeout(() => { btn.innerText = '📄 СКОПИРОВАТЬ ССЫЛКУ'; }, 2000);
        });
    });

    document.getElementById('startGameBtn').addEventListener('click', startGame);

    function startGame() {
        document.getElementById('startMenu').style.display = 'none';
        document.getElementById('gameUI').style.display = 'block';
        if(!gameStarted) {
            gameStarted = true;
            initScene(); // Сначала создаем сцену
            initMultiplayer(); // Потом коннект
            animate();
            renderer.domElement.requestPointerLock();
        }
    }

    const APP_ID = 'e8e01bce-e246-44a2-ab26-9f09c5704b7d';
    let settings = { mouseSens: 2.0, moveSpeed: 0.15, jumpPower: 0.2, crosshairStyle: 'plus', crosshairColor: '#ff0000', crosshairSize: 48, crosshairOpacity: 1 };
    
    let scene, camera, renderer, weaponGroup;
    let bullets = [];
    let enemies = [];
    let keys = {}, yaw = 0, pitch = 0, health = 150, ammo = 30;

    function initScene() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0a); // Убедимся, что фон не просто черный
        scene.fog = new THREE.Fog(0x0a0a0a, 10, 80);
        
        camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
        camera.position.set(0, 2, 5); // Поднимем выше пола
        
        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);

        // Свет
        scene.add(new THREE.AmbientLight(0xffffff, 0.5)); // Больше света
        const dLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dLight.position.set(10, 20, 10);
        scene.add(dLight);
        
        // Пол
        const floor = new THREE.Mesh(
            new THREE.PlaneGeometry(100, 100), 
            new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.8 })
        );
        floor.rotation.x = -Math.PI/2;
        scene.add(floor);
        
        const grid = new THREE.GridHelper(100, 50, 0xff0000, 0x333333);
        scene.add(grid);

        // Столбы
        const boxGeo = new THREE.BoxGeometry(4, 8, 4);
        const boxMat = new THREE.MeshStandardMaterial({ color: 0x444444 });
        for(let i=0; i<20; i++) {
            const pillar = new THREE.Mesh(boxGeo, boxMat);
            pillar.position.set((Math.random()-0.5)*80, 4, (Math.random()-0.5)*80);
            scene.add(pillar);
        }

        // Оружие
        weaponGroup = new THREE.Group();
        const pistolBody = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.4, 1), new THREE.MeshStandardMaterial({ color: 0x111 }));
        pistolBody.position.set(0.6, -0.4, -0.8);
        weaponGroup.add(pistolBody);
        camera.add(weaponGroup);
        scene.add(camera);

        // Враги
        for(let i=0; i<12; i++) spawnEnemy();
    }

    function spawnEnemy() {
        const e = new THREE.Group();
        const body = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2.5, 1.5), new THREE.MeshStandardMaterial({ color: 0xaa0000 }));
        e.add(body);
        e.position.set((Math.random()-0.5)*80, 1.25, (Math.random()-0.5)*80);
        enemies.push({ mesh: e, health: 100, alive: true });
        scene.add(e);
    }

    function createBullet() {
        if(ammo <= 0) return;
        ammo--;
        const b = new THREE.Mesh(new THREE.SphereGeometry(0.15), new THREE.MeshBasicMaterial({ color: 0xffff00 }));
        b.position.copy(camera.position);
        const dir = new THREE.Vector3(0,0,-1).applyQuaternion(camera.quaternion);
        bullets.push({ mesh: b, vel: dir.multiplyScalar(1.2), life: 60 });
        scene.add(b);
    }

    // Мультиплеер
    let photon = null, myId = null, otherPlayers = new Map();
    function initMultiplayer() {
        photon = new Photon.LoadBalancing.LoadBalancingClient(Photon.ConnectionProtocol.Wss, APP_ID, '1.0');
        photon.connectToRegion('eu');
        photon.addEventListener(Photon.LoadBalancing.EventName.CONNECTED_TO_MASTER, () => {
            photon.myActor().setName(myUsername);
            photon.opJoinOrCreateRoom(targetRoomID);
        });
        photon.addEventListener(Photon.LoadBalancing.EventName.JOINED_ROOM, () => {
            myId = photon.myActor().actorNr;
            document.getElementById('status').innerText = '🎮 ' + myUsername;
            updatePlayersCount();
        });
        photon.addEventListener(Photon.LoadBalancing.EventName.ACTOR_JOINED, updatePlayersCount);
        photon.addEventListener(Photon.LoadBalancing.EventName.ACTOR_LEFT, (act) => {
            if(otherPlayers.has(act.actorNr)) { scene.remove(otherPlayers.get(act.actorNr)); otherPlayers.delete(act.actorNr); }
            updatePlayersCount();
        });
        photon.addEventListener(Photon.LoadBalancing.EventName.RAISE_EVENT, (code, data, actorNr) => {
            if(code === 1) {
                if(!otherPlayers.has(actorNr)) {
                    const op = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.4, 1.2), new THREE.MeshStandardMaterial({ color: 0x00aaff }));
                    scene.add(op); otherPlayers.set(actorNr, op);
                }
                const p = otherPlayers.get(actorNr);
                p.position.set(data.x, data.y, data.z); p.rotation.y = data.ry;
            }
        });
    }

    function updatePlayersCount() {
        const c = photon && photon.myRoom() ? photon.actors.count : 1;
        document.getElementById('playersOnline').innerText = c;
        document.getElementById('onlineCount').innerText = c;
    }

    window.addEventListener('keydown', e => { keys[e.code] = true; if(e.code === 'KeyR') ammo = 30; });
    window.addEventListener('keyup', e => keys[e.code] = false);
    window.addEventListener('mousemove', e => {
        if(document.pointerLockElement) {
            yaw -= e.movementX * 0.002 * settings.mouseSens;
            pitch -= e.movementY * 0.002 * settings.mouseSens;
            pitch = Math.max(-1.4, Math.min(1.4, pitch));
            camera.rotation.set(pitch, yaw, 0, 'YXZ');
        }
    });
    window.addEventListener('mousedown', e => { if(document.pointerLockElement) createBullet(); });

    function animate() {
        if(!gameStarted) return;
        requestAnimationFrame(animate);
        
        if(document.pointerLockElement) {
            const speed = settings.moveSpeed;
            const moveDir = new THREE.Vector3();
            if(keys['KeyW']) moveDir.z -= 1; if(keys['KeyS']) moveDir.z += 1;
            if(keys['KeyA']) moveDir.x -= 1; if(keys['KeyD']) moveDir.x += 1;
            moveDir.applyQuaternion(camera.quaternion);
            moveDir.y = 0;
            if(moveDir.length() > 0) camera.position.add(moveDir.normalize().multiplyScalar(speed));
            
            if(photon && photon.myRoom()) {
                photon.raiseEvent(1, { x: camera.position.x, y: camera.position.y, z: camera.position.z, ry: camera.rotation.y });
            }
        }
        
        bullets.forEach((b, i) => {
            b.mesh.position.add(b.vel); b.life--;
            if(b.life <= 0) { scene.remove(b.mesh); bullets.splice(i, 1); }
            else {
                enemies.forEach(e => {
                    if(e.alive && e.mesh.position.distanceTo(b.mesh.position) < 2) {
                        e.alive = false; scene.remove(e.mesh);
                    }
                });
            }
        });

        renderer.render(scene, camera);
        
        document.getElementById('health').innerText = health;
        document.getElementById('ammo').innerText = ammo + '/30';
        document.getElementById('enemyCount').innerText = enemies.filter(e => e.alive).length;
    }

    // Tabs
    document.querySelectorAll('.menu-tab').forEach(t => {
        t.addEventListener('click', () => {
            document.querySelectorAll('.menu-tab').forEach(x => x.classList.remove('active'));
            document.querySelectorAll('.menu-section').forEach(x => x.classList.remove('active'));
            t.classList.add('active'); document.getElementById('tab-' + t.dataset.tab).classList.add('active');
        });
    });

    window.addEventListener('resize', () => {
        if(!camera) return;
        camera.aspect = window.innerWidth/window.innerHeight; camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    </script>
</body>
</html>
"""

with open("c:/Users/Sasha/Downloads/fix11/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

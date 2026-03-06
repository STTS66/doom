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
        #authPanel, #lobbyPanel {
            background: rgba(20,20,30,0.95); border: 3px solid #d97c2b; padding: 40px; border-radius: 15px; width: 350px;
            box-shadow: 0 0 40px #f90; text-align: center;
        }
        #lobbyPanel { display: none; }
        #authPanel h2, #lobbyPanel h2 { color: #f90; margin-top: 0; font-size: 28px; }
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
        #openSettingsBtn { background: #444; border-color: #888; margin-bottom: 0;}
        #openSettingsBtn:hover { background: #666; box-shadow: 0 0 20px #888; }
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
            position: absolute; bottom: 30px; right: 30px; background: rgba(20,20,30,0.95);
            border: 3px solid #d97c2b; padding: 25px; width: 320px; z-index: 2000;
            border-radius: 15px; box-shadow: 0 0 40px #f90; backdrop-filter: blur(10px);
            transition: all 0.3s; display: none;
        }
        #menuPanel h3 { margin: 0 0 20px; color: #f90; text-align: center; font-size: 24px; }
        
        .menu-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #f90; padding-bottom: 10px; }
        .menu-tab { flex: 1; text-align: center; padding: 8px; cursor: pointer; color: #ca9; border-radius: 8px 8px 0 0; transition: all 0.2s; }
        .menu-tab.active { color: #f90; border-bottom: 3px solid #f90; font-weight: bold; }
        .menu-section { display: none; }
        .menu-section.active { display: block; }
        
        .setting-item { margin-bottom: 20px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 8px; }
        .setting-item label { display: block; color: #ffaa00; margin-bottom: 8px; font-size: 16px; }
        .setting-item input[type=range] { width: 100%; height: 8px; background: #333; border-radius: 4px; -webkit-appearance: none; accent-color: #f90; }
        .setting-item input[type=color] { width: 100%; height: 40px; border: 2px solid #f90; border-radius: 8px; background: transparent; cursor: pointer; }
        .setting-item select { width: 100%; padding: 10px; background: #2a1f15; color: #ca9; border: 2px solid #a55; border-radius: 8px; font-size: 16px; }
        .value-display { float: right; color: #7fffd4; font-weight: bold; }
        
        .weapon-selector { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
        .weapon-btn { background: #2a1f15; color: #ca9; border: 2px solid #a55; padding: 12px; cursor: pointer; font-size: 16px; flex: 1 0 45%; border-radius: 8px; transition: all 0.2s; text-align: center; }
        .weapon-btn:hover { background: #b55f2a; color: #fff; border-color: #fd9; }
        .weapon-btn.active { background: #b55f2a; color: #fff; border-color: #fd9; box-shadow: 0 0 20px #f90; }
        
        #status { position: absolute; top: 20px; right: 20px; background: rgba(0,0,0,0.9); padding: 12px 24px; border: 2px solid #0f0; color: #0f0; z-index: 100; border-radius: 30px; font-size: 18px; box-shadow: 0 0 20px #0f0; }
        .instruction { position: absolute; bottom: 20px; left: 20px; background: rgba(0,0,0,0.8); padding: 15px 25px; color: #ffaa00; z-index: 100; border-radius: 30px; border-left: 6px solid #f70; font-size: 18px; box-shadow: 0 0 20px rgba(255,150,0,0.3); }
        #fps-counter { position: absolute; top: 20px; right: 260px; background: rgba(0,0,0,0.7); padding: 8px 15px; border-radius: 20px; color: #0f0; font-size: 18px; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <div id="startMenu">
        <h1 style="color: #f90; font-size: 72px; text-shadow: 0 0 40px #f90; margin-bottom: 40px; font-weight: 900; letter-spacing: 5px;">DOOM 3D</h1>
        
        <div id="authPanel">
            <h2>АВТОРИЗАЦИЯ</h2>
            <div id="authError"></div>
            <input type="text" id="usernameInput" placeholder="Имя пользователя">
            <input type="password" id="passwordInput" placeholder="Пароль">
            <button class="authBtn" id="loginBtn">ВОЙТИ</button>
            <button class="authBtn" id="registerBtn">РЕГИСТРАЦИЯ</button>
            <button class="authBtn" id="openSettingsBtn">НАСТРОЙКИ</button>
        </div>

        <div id="lobbyPanel">
            <h2>ЛОББИ СЕРВЕРА</h2>
            <p style="color: #fff; font-size: 16px; margin-bottom: 15px;">Пригласи друга по этой ссылке:</p>
            <div style="background: #111; padding: 12px; border: 2px dashed #f90; border-radius: 8px; color: #ffaa00; margin-bottom: 20px; word-break: break-all; user-select: text;" id="inviteLink"></div>
            <button class="authBtn" id="copyLinkBtn">📄 СКОПИРОВАТЬ ССЫЛКУ</button>
            <button class="authBtn" id="startGameBtn" style="background: #0a0; border-color: #0f0; box-shadow: 0 0 20px rgba(0,255,0,0.3);">🎮 ПРИСОЕДИНИТЬСЯ / НАЧАТЬ</button>
        </div>
    </div>

    <div id="gameUI">
        <div id="info">❤️ <span id="health">150</span> 🔫 <span id="ammo">30/30</span> 👥 <span id="playersOnline">1</span>/8</div>
        <div id="fps-counter">FPS: <span id="fpsValue">60</span></div>
        <div id="status">🔄 ОЖИДАНИЕ...</div>
        <div id="crosshair">+</div>
        <div class="instruction">WASD — ходьба | ПРОБЕЛ — прыжок | ЛКМ — огонь | ПКМ — прицел | R — перезарядка | SHIFT — бег | ESC — курсор / меню</div>
    </div>
    
    <div id="menuPanel">
        <button id="closeSettingsBtn" style="position: absolute; top: 10px; right: 10px; background: #a55; border: none; color: #fff; cursor: pointer; border-radius: 5px; padding: 5px 10px;">X</button>
        <h3>⚡ МЕНЮ НАСТРОЕК ⚡</h3>
        
        <div class="menu-tabs">
            <div class="menu-tab active" data-tab="weapons">🔫 ОРУЖИЕ</div>
            <div class="menu-tab" data-tab="aim">🎯 ПРИЦЕЛ</div>
            <div class="menu-tab" data-tab="game">⚙️ УПРАВЛЕНИЕ</div>
        </div>
        
        <div class="menu-section active" id="tab-weapons">
            <div class="weapon-selector">
                <button class="weapon-btn active" id="wpPistol">🔫 ПИСТОЛЕТ</button>
                <button class="weapon-btn" id="wpShotgun">🔫🔫 ДРОБОВИК</button>
                <button class="weapon-btn" id="wpRifle">⚡ ВИНТОВКА</button>
                <button class="weapon-btn" id="wpRocket">💥 РОКЕТНИЦА</button>
            </div>
            <div style="margin-top: 20px; color: #ffaa00; font-size: 18px;">
                👾 ВРАГОВ: <span id="enemyCount">12</span><br>
                🏆 УРОВЕНЬ: <span id="level">1</span><br>
                🟢 ОНЛАЙН: <span id="onlineCount">1</span>/8
            </div>
        </div>
        
        <div class="menu-section" id="tab-aim">
            <div class="setting-item">
                <label>🎯 ФОРМА ПРИЦЕЛА <span class="value-display" id="crosshairStyleVal">Плюс</span></label>
                <select id="crosshairStyle"><option value="plus" selected>➕ Плюс</option><option value="dot">• Точка</option><option value="circle">○ Круг</option><option value="cross">✖ Крест</option></select>
            </div>
            <div class="setting-item"><label>🔴 ЦВЕТ ПРИЦЕЛА</label><input type="color" id="crosshairColor" value="#ff0000"></div>
            <div class="setting-item"><label>📏 РАЗМЕР ПРИЦЕЛА <span class="value-display" id="crosshairSizeVal">48</span></label><input type="range" id="crosshairSize" min="24" max="72" value="48" step="2"></div>
            <div class="setting-item"><label>✨ ПРОЗРАЧНОСТЬ <span class="value-display" id="crosshairOpacityVal">100%</span></label><input type="range" id="crosshairOpacity" min="0.3" max="1" value="1" step="0.1"></div>
        </div>
        
        <div class="menu-section" id="tab-game">
            <div class="setting-item"><label>🖱️ ЧУВСТВИТЕЛЬНОСТЬ <span class="value-display" id="sensVal">2.0</span></label><input type="range" id="mouseSens" min="0.5" max="5.0" value="2.0" step="0.1"></div>
            <div class="setting-item"><label>🏃 СКОРОСТЬ БЕГА <span class="value-display" id="speedVal">0.15</span></label><input type="range" id="moveSpeed" min="0.1" max="0.3" value="0.15" step="0.01"></div>
            <div class="setting-item"><label>🦘 СИЛА ПРЫЖКА <span class="value-display" id="jumpVal">0.2</span></label><input type="range" id="jumpPower" min="0.1" max="0.4" value="0.2" step="0.01"></div>
            <div class="setting-item"><label>🎮 ПОКАЗЫВАТЬ FPS</label><select id="showFPS"><option value="yes" selected>✅ Да</option><option value="no">❌ Нет</option></select></div>
        </div>
        
        <div style="margin-top: 15px; text-align: center;">
            <button id="quitGameBtn" style="background: #a00; color: #fff; border: 2px solid #f55; padding: 10px 20px; font-weight: bold; font-size: 16px; border-radius: 5px; cursor: pointer; width: 100%; transition: 0.2s;" onmouseover="this.style.background='#c00';" onmouseout="this.style.background='#a00';">🛑 ВЫЙТИ В ГЛАВНОЕ МЕНЮ</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.photonengine.com/api/sdk/4.1.12.1/photon-sdk.min.js"></script>

    <script>
    const API_URL = window.location.origin;
    let myUsername = '';
    let gameStarted = false;
    let targetRoomID = 'DOOM_ARENA_GLOBAL'; // По умолчанию

    // Проверка приглашения в URL
    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams.get('room')) {
        targetRoomID = urlParams.get('room');
    } else {
        targetRoomID = 'ROOM_' + Math.random().toString(36).substring(2, 9).toUpperCase();
    }

    const authError = document.getElementById('authError');
    const uInput = document.getElementById('usernameInput');
    const pInput = document.getElementById('passwordInput');

    async function handleAuth(endpoint) {
        if(!uInput.value || !pInput.value) { authError.innerText = 'Заполните поля'; return; }
        try {
            const res = await fetch(API_URL + endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: uInput.value, password: pInput.value })
            });
            const data = await res.json();
            if(!res.ok) { authError.innerText = data.error || 'Ошибка'; }
            else { 
                myUsername = data.username || uInput.value;
                showLobby();
            }
        } catch(e) {
            authError.innerText = 'Ошибка соединения с сервером!';
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
        
        // Генерируем ссылку
        const link = window.location.origin + window.location.pathname + "?room=" + targetRoomID;
        document.getElementById('inviteLink').innerText = link;
    }

    document.getElementById('copyLinkBtn').addEventListener('click', () => {
        const link = document.getElementById('inviteLink').innerText;
        navigator.clipboard.writeText(link).then(() => {
            const btn = document.getElementById('copyLinkBtn');
            btn.innerText = '✅ ССЫЛКА СКОПИРОВАНА!';
            btn.style.background = '#0a0';
            setTimeout(() => {
                btn.innerText = '📄 СКОПИРОВАТЬ ССЫЛКУ';
                btn.style.background = '#b55f2a';
            }, 2000);
        });
    });

    document.getElementById('startGameBtn').addEventListener('click', () => {
        startGame();
    });

    function startGame() {
        document.getElementById('startMenu').style.display = 'none';
        document.getElementById('gameUI').style.display = 'block';
        if(!gameStarted) {
            gameStarted = true;
            initMultiplayer();
            animate();
            renderer.domElement.requestPointerLock = renderer.domElement.requestPointerLock || renderer.domElement.mozRequestPointerLock;
            renderer.domElement.requestPointerLock();
        }
    }

    // ВАШ APPID
    const APP_ID = 'e8e01bce-e246-44a2-ab26-9f09c5704b7d';
    
    // ===== НАСТРОЙКИ ПО УМОЛЧАНИЮ =====
    let settings = { mouseSens: 2.0, moveSpeed: 0.15, jumpPower: 0.2, crosshairStyle: 'plus', crosshairColor: '#ff0000', crosshairSize: 48, crosshairOpacity: 1, showFPS: 'yes' };
    
    // ===== УЛУЧШЕННАЯ ГРАФИКА =====
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0f14);
    scene.fog = new THREE.Fog(0x0a0f14, 30, 100);
    
    const camera = new THREE.PerspectiveCamera(80, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 2, 5);
    
    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ReinhardToneMapping; renderer.toneMappingExposure = 1.2;
    document.body.appendChild(renderer.domElement);

    // Particles
    const particleGeo = new THREE.BufferGeometry(); const particleCount = 1000;
    const positions = new Float32Array(particleCount * 3); const colors = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
        positions[i*3] = (Math.random() - 0.5) * 200; positions[i*3+1] = Math.random() * 50; positions[i*3+2] = (Math.random() - 0.5) * 200;
        colors[i*3] = 1.0; colors[i*3+1] = 0.3 + Math.random() * 0.5; colors[i*3+2] = 0.1;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3)); particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    scene.add(new THREE.Points(particleGeo, new THREE.PointsMaterial({ size: 0.3, vertexColors: true, transparent: true, opacity: 0.4, blending: THREE.AdditiveBlending })));

    // Environment
    scene.add(new THREE.AmbientLight(0x404060, 0.6));
    const dirLight = new THREE.DirectionalLight(0xffeedd, 1.5); dirLight.position.set(20, 40, 20); dirLight.castShadow = true; scene.add(dirLight);
    
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x3a2e22, roughness: 0.8 });
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), floorMat); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
    scene.add(new THREE.GridHelper(80, 40, 0xaa8866, 0x664422));

    const wallMat = new THREE.MeshStandardMaterial({ color: 0x7a5a3a });
    const walls = [
        { x: 0, z: -40, w: 82, d: 2 }, { x: 0, z: 40, w: 82, d: 2 },
        { x: -40, z: 0, w: 2, d: 82 }, { x: 40, z: 0, w: 2, d: 82 }
    ];
    walls.forEach(w => {
        const wall = new THREE.Mesh(new THREE.BoxGeometry(w.w, 10, w.d), wallMat);
        wall.position.set(w.x, 5, w.z); wall.castShadow = wall.receiveShadow = true; scene.add(wall);
    });

    for (let x = -30; x <= 30; x += 10) {
        for (let z = -30; z <= 30; z += 10) {
            if (Math.random() > 0.3) {
                const pillar = new THREE.Mesh(new THREE.CylinderGeometry(1, 1.2, 8), new THREE.MeshStandardMaterial({ color: 0x885533, emissive: 0x221100 }));
                pillar.position.set(x, 4, z); pillar.castShadow = pillar.receiveShadow = true; scene.add(pillar);
            }
        }
    }

    function createEnemy(x, z) {
        const group = new THREE.Group();
        const base = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.8, 1.6), new THREE.MeshStandardMaterial({ color: 0x8a3a2a, emissive: 0x110000 }));
        base.position.y = 0.6; base.castShadow = true; group.add(base);
        const head = new THREE.Mesh(new THREE.DodecahedronGeometry(0.7), new THREE.MeshStandardMaterial({ color: 0x9a5a3a }));
        head.position.y = 1.8; head.castShadow = true; group.add(head);
        const eye = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.15, 0.15), new THREE.MeshStandardMaterial({ color: 0xff0000, emissive: 0xff0000 }));
        eye.position.set(0, 1.8, 0.7); group.add(eye);
        group.position.set(x, 0, z); group.userData = { head: head, eye: eye, offset: Math.random() * 100 };
        return group;
    }

    const enemies = [];
    for (let i = 0; i < 12; i++) {
        const angle = (i / 12) * Math.PI * 2; const radius = 20 + Math.random() * 15;
        const enemy = createEnemy(Math.cos(angle) * radius, Math.sin(angle) * radius); scene.add(enemy);
        enemies.push({ mesh: enemy, health: 100, alive: true, speed: 0.03 + Math.random() * 0.03 });
    }

    // Weapons
    const weaponGroup = new THREE.Group(); camera.add(weaponGroup); scene.add(camera);
    const materials = {
        steel: new THREE.MeshStandardMaterial({ color: 0xcccccc, roughness: 0.3 }),
        darkSteel: new THREE.MeshStandardMaterial({ color: 0x666666, roughness: 0.2 }),
        wood: new THREE.MeshStandardMaterial({ color: 0x8B4513, roughness: 0.9 })
    };

    function createPistol() {
        weaponGroup.clear();
        const body = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.25, 1.0), materials.steel); body.position.set(0.5, -0.2, -0.6); weaponGroup.add(body);
        const handle = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.7, 0.3), materials.wood); handle.position.set(0.5, -0.7, -0.3); weaponGroup.add(handle);
        const barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.9), materials.darkSteel); barrel.rotation.x = Math.PI/2; barrel.position.set(0.5, -0.1, -1.1); weaponGroup.add(barrel);
    }
    createPistol();

    const bullets = [];
    function createBullet(startPos, direction) {
        const bullet = new THREE.Mesh(new THREE.SphereGeometry(0.1), new THREE.MeshStandardMaterial({ color: 0xffaa00, emissive: 0x442200 }));
        bullet.position.copy(startPos); scene.add(bullet);
        bullets.push({ mesh: bullet, velocity: direction.clone().multiplyScalar(0.8), life: 60 });
    }

    function updateBullets() {
        for (let i = bullets.length - 1; i >= 0; i--) {
            const b = bullets[i]; b.mesh.position.add(b.velocity); b.life--;
            for (let j = 0; j < enemies.length; j++) {
                const enemy = enemies[j]; if (!enemy.alive) continue;
                if (b.mesh.position.distanceTo(enemy.mesh.position) < 1.5) {
                    enemy.health -= 25;
                    if (enemy.health <= 0) { enemy.alive = false; scene.remove(enemy.mesh); }
                    scene.remove(b.mesh); bullets.splice(i, 1); break;
                }
            }
            if (b.life <= 0) { scene.remove(b.mesh); bullets.splice(i, 1); }
        }
    }

    // Мультиплеер
    let photon = null; let myId = null; let otherPlayers = new Map();
    function createNicknameSprite(name) {
        const canvas = document.createElement('canvas'); canvas.width = 512; canvas.height = 128;
        const ctx = canvas.getContext('2d');
        ctx.font = 'bold 50px Arial'; ctx.textAlign = 'center'; ctx.fillStyle = '#10FFa0';
        ctx.strokeStyle = '#000000'; ctx.lineWidth = 6;
        ctx.strokeText(name, 256, 64); ctx.fillText(name, 256, 64);
        const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(canvas), transparent: true }));
        sprite.scale.set(4, 1, 1); sprite.position.y = 3.2; return sprite;
    }

    function initMultiplayer() {
        try {
            photon = new Photon.LoadBalancing.LoadBalancingClient(Photon.ConnectionProtocol.Wss, APP_ID, '1.0');
            photon.connectToRegion('eu');
            
            photon.addEventListener(Photon.LoadBalancing.EventName.CONNECTED_TO_MASTER, () => {
                document.getElementById('status').innerText = '🟢 ПОДКЛЮЧЕНИЕ К КОМНАТЕ...';
                photon.myActor().setName(myUsername);
                photon.opJoinRoom(targetRoomID); // Пытаемся зайти в комнату по ссылке
            });
            
            photon.addEventListener(Photon.LoadBalancing.EventName.JOIN_ROOM_FAILED, () => {
                // Если комнаты нет, создаем новую с этим айди
                photon.opCreateRoom(targetRoomID, { maxPlayers: 8 });
            });
            
            photon.addEventListener(Photon.LoadBalancing.EventName.JOINED_ROOM, () => {
                document.getElementById('status').innerText = '🎮 В ИГРЕ [' + targetRoomID + ']';
                myId = photon.myActor().actorNr;
                photon.actors.getAll().forEach(act => { if (!act.isLocal) createOtherPlayer(act.actorNr, act.name); });
                updatePlayersCount();
            });
            
            photon.addEventListener(Photon.LoadBalancing.EventName.ACTOR_JOINED, (act) => {
                if (!act.isLocal) createOtherPlayer(act.actorNr, act.name);
                updatePlayersCount();
            });
            
            photon.addEventListener(Photon.LoadBalancing.EventName.ACTOR_LEFT, (act) => {
                if(otherPlayers.has(act.actorNr)) { scene.remove(otherPlayers.get(act.actorNr).mesh); otherPlayers.delete(act.actorNr); }
                updatePlayersCount();
            });
            
            photon.addEventListener(Photon.LoadBalancing.EventName.RAISE_EVENT, (code, data, actorNr) => {
                const p = otherPlayers.get(actorNr); if (!p) return;
                if (code === 1) { p.mesh.position.set(data.x, data.y, data.z); p.mesh.rotation.y = data.rotY; }
            });
        } catch(e) { document.getElementById('status').innerText = '⚠️ ОФФЛАЙН'; }
    }

    function createOtherPlayer(id, nameStr) {
        if(otherPlayers.has(id)) return;
        const name = nameStr || "Игрок";
        const group = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.8, 2.0), new THREE.MeshStandardMaterial({ color: 0x3366ff }));
        body.position.y = 1.0; group.add(body);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.5), new THREE.MeshStandardMaterial({ color: 0x44aaff }));
        head.position.y = 2.2; group.add(head);
        group.add(createNicknameSprite(name));
        scene.add(group); otherPlayers.set(id, { mesh: group });
    }

    function updatePlayersCount() {
        const count = photon && photon.myRoom() ? photon.actors.count : 1;
        document.getElementById('playersOnline').innerText = count; document.getElementById('onlineCount').innerText = count;
    }

    // Player logic
    let health = 150, ammo = 30, maxAmmo = 30; let isReloading = false;
    let keys = {}, mouseX = 0, mouseY = 0, pitch = 0, yaw = 0, velocityY = 0, onGround = true, gravity = 0.02;

    window.addEventListener('keydown', (e) => { 
        keys[e.code] = true; 
        if(e.code === 'Escape' && gameStarted) { document.exitPointerLock(); document.getElementById('menuPanel').style.display = 'block'; }
        if(e.code === 'KeyR' && !isReloading) { isReloading = true; setTimeout(() => { ammo = maxAmmo; isReloading = false; updateUI(); }, 1000); }
    });
    window.addEventListener('keyup', (e) => { keys[e.code] = false; });
    window.addEventListener('mousemove', (e) => {
        if (document.pointerLockElement === renderer.domElement) {
            yaw -= e.movementX * 0.002 * settings.mouseSens; pitch -= e.movementY * 0.002 * settings.mouseSens;
            pitch = Math.max(-1.4, Math.min(1.4, pitch));
            camera.rotation.order = 'YXZ'; camera.rotation.y = yaw; camera.rotation.x = pitch;
        }
    });
    renderer.domElement.addEventListener('click', () => { if(gameStarted) renderer.domElement.requestPointerLock(); });
    renderer.domElement.addEventListener('mousedown', (e) => {
        if (e.button === 0 && document.pointerLockElement === renderer.domElement && ammo > 0 && !isReloading) {
            ammo--; const dir = camera.getWorldDirection(new THREE.Vector3());
            createBullet(camera.position.clone().add(dir.clone().multiplyScalar(1.5)), dir); updateUI();
            weaponGroup.position.z += 0.1; setTimeout(() => weaponGroup.position.z -= 0.1, 50);
        }
        if (e.button === 2) { camera.fov = 50; camera.updateProjectionMatrix(); }
    });
    renderer.domElement.addEventListener('mouseup', (e) => {
        if (e.button === 2) { camera.fov = 80; camera.updateProjectionMatrix(); }
    });
    renderer.domElement.addEventListener('contextmenu', e => e.preventDefault());

    function updateUI() {
        document.getElementById('health').innerText = health; document.getElementById('ammo').innerText = ammo + '/' + maxAmmo;
        document.getElementById('enemyCount').innerText = enemies.filter(e => e.alive).length;
    }

    function handleMovement() {
        const speed = keys['ShiftLeft'] ? settings.moveSpeed * 1.5 : settings.moveSpeed;
        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion); forward.y = 0; forward.normalize();
        const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
        if (keys['KeyW']) camera.position.addScaledVector(forward, speed);
        if (keys['KeyS']) camera.position.addScaledVector(forward, -speed);
        if (keys['KeyA']) camera.position.addScaledVector(right, -speed);
        if (keys['KeyD']) camera.position.addScaledVector(right, speed);
        if (keys['Space'] && onGround) { velocityY = settings.jumpPower; onGround = false; }
        
        camera.position.y += velocityY; velocityY -= gravity;
        if (camera.position.y <= 1.0) { camera.position.y = 1.0; velocityY = 0; onGround = true; }
        camera.position.x = Math.max(-38, Math.min(38, camera.position.x)); camera.position.z = Math.max(-38, Math.min(38, camera.position.z));
    }

    let frames = 0, lastTime = performance.now();
    function animate() {
        requestAnimationFrame(animate);
        if (document.pointerLockElement === renderer.domElement) handleMovement();
        if (photon && photon.myRoom() && myId) photon.raiseEvent(1, { x: camera.position.x, y: camera.position.y, z: camera.position.z, rotY: camera.rotation.y });
        
        updateBullets(); 
        enemies.forEach(e => {
            if(!e.alive) return;
            const p = camera.position, ePos = e.mesh.position, dx = p.x - ePos.x, dz = p.z - ePos.z, dist = Math.sqrt(dx*dx + dz*dz);
            e.mesh.userData.head.rotation.y += 0.05; e.mesh.userData.head.position.y = 1.8 + Math.sin(frames * 0.1 + e.mesh.userData.offset) * 0.2;
            e.mesh.userData.eye.position.y = e.mesh.userData.head.position.y;
            if (dist < 20) { ePos.x += (dx / dist) * e.speed; ePos.z += (dz / dist) * e.speed; e.mesh.lookAt(p.x, ePos.y, p.z); }
        });
        updateUI();
        
        frames++; const now = performance.now();
        if (now - lastTime >= 1000) { document.getElementById('fpsValue').innerText = frames; frames = 0; lastTime = now; }
        renderer.render(scene, camera);
    }
    
    // UI Init (crosshair settings)
    const chEl = document.getElementById('crosshair');
    function uCross() {
        let sym = '+'; switch(settings.crosshairStyle) { case 'plus': sym = '+'; break; case 'dot': sym = '•'; break; case 'circle': sym = '○'; break; case 'cross': sym = '✖'; break; }
        chEl.innerText = sym; chEl.style.color = settings.crosshairColor; chEl.style.fontSize = settings.crosshairSize + 'px'; chEl.style.opacity = settings.crosshairOpacity;
    }
    document.querySelectorAll('.menu-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.menu-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.menu-section').forEach(s => s.classList.remove('active'));
            tab.classList.add('active'); document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
        });
    });
    document.getElementById('crosshairStyle').addEventListener('change', e => { settings.crosshairStyle = e.target.value; uCross(); });
    document.getElementById('crosshairColor').addEventListener('input', e => { settings.crosshairColor = e.target.value; uCross(); });
    document.getElementById('crosshairSize').addEventListener('input', e => { settings.crosshairSize = e.target.value; uCross(); });
    document.getElementById('crosshairOpacity').addEventListener('input', e => { settings.crosshairOpacity = e.target.value; uCross(); });
    document.getElementById('mouseSens').addEventListener('input', e => { settings.mouseSens = parseFloat(e.target.value); document.getElementById('sensVal').innerText = settings.mouseSens.toFixed(1); });
    document.getElementById('moveSpeed').addEventListener('input', e => { settings.moveSpeed = parseFloat(e.target.value); document.getElementById('speedVal').innerText = settings.moveSpeed.toFixed(2); });
    document.getElementById('jumpPower').addEventListener('input', e => { settings.jumpPower = parseFloat(e.target.value); document.getElementById('jumpVal').innerText = settings.jumpPower.toFixed(2); });
    document.getElementById('showFPS').addEventListener('change', e => { document.getElementById('fps-counter').style.display = e.target.value === 'yes' ? 'block' : 'none'; });

    window.addEventListener('resize', () => { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight); });
    updateUI();
    </script>
</body>
</html>
"""

with open("c:/Users/Sasha/Downloads/fix11/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# 🔱 Cómo usar este repo (si lo forkeaste)

Este proyecto genera automáticamente una tabla en tu README.md con tus seguidores más
seguidos de GitHub (los que tienen más followers propios), usando la API oficial de
GitHub — sin scraping ni Selenium.

Sigue estos pasos para dejarlo funcionando en tu propio perfil.

---

## 1. Estructura del repo

Asegúrate de que tu fork tenga esta estructura:

```
tu-repo/
├── .github/workflows/update_readme.yml
├── scripts/update_readme.py
└── README.md
```

---

## 2. Agrega los marcadores en tu README.md

Abre tu `README.md` y pega estos dos comentarios en el lugar donde quieras que
aparezca la tabla de seguidores:

```md
<!-- FOLLOWERS_LIST_START -->
<!-- FOLLOWERS_LIST_END -->
```

⚠️ **Importante:** si no agregas estos marcadores, el script fallará porque no sabe
dónde insertar la tabla.

---

## 3. Qué debes cambiar en el workflow

Abre `.github/workflows/update_readme.yml` y revisa/edita lo siguiente:

### a) Nombre y email para los commits

Por defecto los commits quedan a nombre del bot de Actions. Si quieres que aparezcan
con tu usuario, cambia estas dos líneas al final del archivo:

```yaml
git config --global user.name 'TU_USUARIO'
git config --global user.email 'TU_ID+TU_USUARIO@users.noreply.github.com'
```

**¿Cómo saber tu `TU_ID`?** Ve a GitHub → **Settings → Emails** en tu cuenta, ahí
aparece tu email `noreply` completo con el formato `123456+usuario@users.noreply.github.com`.
Cópialo tal cual.

Si no te importa que el commit quede como del bot, puedes dejar esas líneas
como están (no es obligatorio cambiarlas).

### b) Cantidad de seguidores a mostrar (opcional)

```yaml
MAX_FOLLOWER_COUNT: 10
```

Cambia el `10` por el número que quieras (ej. `5`, `20`, etc).

### c) `GITHUB_USER_NAME` — normalmente NO hay que tocarlo

```yaml
GITHUB_USER_NAME: ${{ github.repository_owner }}
```

Esto toma automáticamente el dueño del repo. Solo cámbialo si quieres generar la
tabla para un usuario distinto al dueño del repo (poco común).

---

## 4. Permisos del repo (revisar una vez)

Ve a **Settings → Actions → General** en tu repo → baja hasta **"Workflow permissions"**
→ asegúrate de que esté marcada la opción **"Read and write permissions"**.

Sin esto, el workflow no podrá hacer `git push` del README actualizado.

---

## 5. Probarlo

1. Ve a la pestaña **Actions** de tu repo.
2. Si aparece un aviso para habilitar Actions en el fork, acéptalo.
3. Selecciona el workflow **"Update README with Top Followers"**.
4. Haz clic en **"Run workflow"** → confirma.
5. Espera un par de minutos (consulta la API por cada seguidor, así que si tienes
   muchos, tarda un poco más).
6. Revisa tu `README.md` — debería aparecer la tabla actualizada con fecha y hora.

---

## 6. ¿Quieres que aparezca en tu perfil de GitHub?

Solo el repo con el **mismo nombre que tu usuario** (ej. si tu usuario es `NachoOFC`,
el repo debe llamarse `NachoOFC/NachoOFC`) se muestra automáticamente en tu perfil
público. Si tu fork tiene otro nombre, el README solo se ve entrando directo al repo.

---

## 7. Frecuencia de ejecución

Por defecto corre **una vez al día a medianoche UTC**:

```yaml
schedule:
  - cron: '0 0 * * *'
```

Puedes cambiar el horario editando el cron, o simplemente ejecutarlo manualmente
cuando quieras desde la pestaña Actions.

---

## ❓ Problemas comunes

| Problema | Causa probable |
| --- | --- |
| El workflow no corre solo | Actions deshabilitadas en el fork, o el cron se desactivó por 60 días de inactividad del repo |
| Falla el `git push` | Falta activar "Read and write permissions" en Settings → Actions |
| No aparece la tabla | Faltan los marcadores `FOLLOWERS_LIST_START` / `FOLLOWERS_LIST_END` en el README |
| Tarda mucho en correr | Normal si tienes muchos seguidores — el script consulta la API una vez por cada uno |

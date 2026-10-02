# NetBox con branding Livinnet (Dokploy)

Imagen oficial `netboxcommunity/netbox` + logos de Livinnet. No toca código, BD ni configuración.

## Qué cambia
| Dónde | Archivo (en `/opt/netbox/netbox/static/`) |
|---|---|
| Logo sidebar y login, tema claro | `logo_netbox_dark_teal.svg` |
| Logo sidebar y login, tema oscuro | `logo_netbox_bright_teal.svg` |
| Favicon | `netbox.ico` |
| Icono Apple/iOS | `netbox_touch-icon-180.png` |
| Favicon de `/api/` | `rest-api.ico` |

Los SVG son un envoltorio del PNG (no vectoriales). Si se consigue el SVG original, reemplazarlos tal cual en `branding/`.

## Dokploy
Servicio **Compose** → Provider **Git** → repo `c4rlos-mor4n/netbox-docker`, rama de despliegue,
**Compose Path** `./livinnet/docker-compose.yml`. Las variables (`SECRET_KEY`, contraseñas, etc.) siguen en la pestaña Environment.
Dokploy construye la imagen en cada deploy (`build:`); los volúmenes existentes no se tocan.

## Actualizar NetBox
Cambiar `NETBOX_VERSION` y redesplegar. Si cambian los nombres de archivos estáticos entre versiones, revisar `templates/base/layout.html` y `login.html` upstream.

## Regenerar assets
`pip install pillow && python3 build-branding.py` (usa `logo-source.png`).

## Rollback
Volver `image:` a `docker.io/netboxcommunity/netbox:${NETBOX_VERSION}` y quitar `build:`.

## Pendiente (fuera de alcance)
El título de pestaña sigue diciendo "| NetBox" y bajo el logo aparece el texto "COMMUNITY" (edición): ambos vienen de templates/código, no de archivos estáticos.

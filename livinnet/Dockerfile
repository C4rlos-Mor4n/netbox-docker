# Imagen oficial de NetBox + branding Livinnet.
# Solo sobrescribe archivos estáticos ya colectados (collectstatic corre en el
# build de la imagen oficial); no toca código, migraciones ni configuración.
ARG NETBOX_VERSION=v4.7-5.1.1
FROM docker.io/netboxcommunity/netbox:${NETBOX_VERSION}

COPY branding/ /opt/netbox/netbox/static/

LABEL org.opencontainers.image.title="NetBox (Livinnet branding)" \
      org.opencontainers.image.vendor="KRIONIXTECH"

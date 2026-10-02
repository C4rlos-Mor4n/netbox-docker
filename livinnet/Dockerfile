# Imagen oficial de NetBox + branding Livinnet.
# Solo sobrescribe/extiende archivos estáticos ya colectados (collectstatic corre en el
# build de la imagen oficial); no toca código, migraciones ni configuración.
ARG NETBOX_VERSION=v4.7-5.1.1
FROM docker.io/netboxcommunity/netbox:${NETBOX_VERSION}

COPY branding/ /opt/netbox/netbox/static/

# Tema de colores: se agrega al final del CSS principal (falla el build si cambia el nombre).
RUN test -f /opt/netbox/netbox/static/netbox.css \
    && cat /opt/netbox/netbox/static/livinnet.css >> /opt/netbox/netbox/static/netbox.css

LABEL org.opencontainers.image.title="NetBox (Livinnet branding)" \
      org.opencontainers.image.vendor="KRIONIXTECH"

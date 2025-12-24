# cpstudio python 3.12


# desde bash Compila los archivos .po a .mo
msgfmt locales/es/LC_MESSAGES/messages.po -o locales/es/LC_MESSAGES/messages.mo
msgfmt locales/en/LC_MESSAGES/messages.po -o locales/en/LC_MESSAGES/messages.mo




> `duplicate key value violates unique constraint "usuarios_pkey"`
**Resumen del error y causa**

Se presenta el error:

> `duplicate key value violates unique constraint "usuarios_pkey"`
>
> `Key (idusuario)=(1) already exists`

Este error ocurre cuando se intenta insertar un registro en la tabla **usuarios** y el valor de la clave primaria (`idusuario`) ya existe.
La causa más común es que el **sequence** asociado a la columna autoincremental (`idusuario`) no está sincronizado con los datos reales de la tabla, algo que suele suceder al **crear nuevos esquemas copiando datos o restaurando estructuras**.

---

**Solución / prevención al crear nuevos esquemas**

Al crear un nuevo esquema o cargar datos manualmente, es necesario **ajustar el sequence** de la clave primaria para que apunte al siguiente valor disponible:

```sql
SELECT setval(
    'master.usuarios_idusuario_seq',
    (SELECT MAX(idusuario) FROM master.usuarios)
);
```

Esto garantiza que los próximos `INSERT` usen un ID válido y evita conflictos de clave primaria.

---

**Recomendación**

Siempre que se cree un nuevo esquema o se migren datos:

* Verificar que **todas las secuencias (`SEQUENCE`) estén alineadas** con los valores existentes en sus tablas.
* Especial atención a tablas maestras como `usuarios`.



## DOCKER CLOUD
Paso 4: Construir y Subir la Imagen
Usaremos Cloud Build, que es la forma más rápida porque Google construye la imagen directamente en la nube por ti.

Ejecuta este comando desde la carpeta de tu proyecto:

Bash

gcloud builds submit --tag us-central1-docker.pkg.dev/akadmia/akdmia-repo/flask-app .
(Reemplaza ID-DE-TU-PROYECTO con tu ID real de Google Cloud).

Paso 5: Desplegar en Cloud Run
Una vez que la imagen está cargada, ponla en marcha con este comando:

Bash




gcloud run deploy flask-service \
    --image us-central1-docker.pkg.dev/akadmia/akdmia-repo/flask-app \
    --set-env-vars "JWT_SECRET_KEY=Myvhyp-wustuj-noqky4,APP_NAME=Akdmia,DATABASE_URL=postgresql://neondb_owner:npg_fFT1cLH8gjuy@ep-morning-wildflower-addmvwux.c-2.us-east-1.aws.neon.tech:5432/AKDMIA?sslmode=require,SECRET_KEY=kacHex-xottak-2tahty,FRONTEND_URL=https://flask-service-akadmia.a.run.app,MAIL_SERVER=smtp.gmail.com, MAIL_PORT=587,MAIL_USE_TLS=true,MAIL_USERNAME=esmerlinep@gmail.com,MAIL_PASSWORD=xqgkhsipfpmtqbau,MAIL_DEFAULT_SENDER=Akdmia <esmerlinep@gmail.com>,SQLALCHEMY_DATABASE_URI=postgresql://neondb_owner:npg_fFT1cLH8gjuy@ep-morning-wildflower-addmvwux.c-2.us-east-1.aws.neon.tech:5432/AKDMIA?sslmode=require" \
    --region us-central1 \
    --allow-unauthenticated

Al terminar, Google te entregará una URL pública (ej. https://flask-service-xyz.a.run.app) donde podrás ver tu aplicación funcionando.

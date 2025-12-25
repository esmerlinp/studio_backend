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






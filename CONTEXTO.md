# CONTEXTO.md - Guía para Agentes Nuevos

## 🎯 QUÉ ES ESTE PROYECTO

Sistema de gestión de inventario para tienda de dulces mexicanos. Aplicación web con backend Django REST y frontend Reflex. Proyecto práctico usado para aprender arquitectura completa y buenas prácticas profesionales.

---

## 📂 ESTRUCTURA DEL PROYECTO

**Directorio raíz:** `/home/lila/Escritorio/R/Tienda.worktrees/agents-profitable-skink`

**Backend:** Carpeta BACKEND con Django REST API
- Modelos: ListaProducto con campos nombre, descripción, precio, cantidad, fecha_de_registro
- Vistas: CRUD completo con endpoints GET, POST, PUT, DELETE
- Serializadores: Convierte modelos a JSON y valida datos
- Base de datos: SQLite local para desarrollo

**Frontend:** Carpeta TIENDA_FRONTED con Reflex framework
- Interfaz reactiva con componentes reutilizables
- Gestión de estado centralizado
- Tabla de productos con paginación
- Modal para crear y editar productos
- Búsqueda y filtrado de productos

---

## 🔧 TECNOLOGÍAS USADAS

**Backend:** Django 6.0, Django REST Framework, SQLite, JWT para autenticación

**Frontend:** Reflex 0.8.26, Python puro sin JavaScript

**Testing:** pytest, factory-boy, faker para generación de datos

**DevOps:** Git para control de versiones, GitHub como repositorio remoto

---

## ✅ QUÉ SE COMPLETÓ EN ESTA SESIÓN

### 1. Implementación del Proyecto Base
Se exploró estructura existente del proyecto y se identificaron problemas. Proyecto estaba 80 por ciento completo pero faltaba configuración y bugfixes.

### 2. Configuración Inicial
Se creó archivo .env con variables de entorno para Django. Se agregó gitignore en raíz y carpeta frontend para excluir entornos virtuales. Se instalaron dependencias de testing en requirements.txt.

### 3. Suite de Tests Completa
Se implementaron setenta tests siguiendo metodología TDD: test primero, luego código, luego refactor.

**Desglose de tests:**
- Diecisiete tests para modelo ListaProducto: creación, validaciones, defaults, ordenamiento, operaciones CRUD
- Dieciséis tests para serializador: transformación de datos, validación, lectura, escritura, casos especiales
- Quince tests para vistas GET: listado, detalle, errores, formatos, tipos de datos
- Trece tests para vistas POST: creación, validación, errores, campos opcionales
- Cinco tests para vistas PUT: actualización, validación, errores
- Cuatro tests para vistas DELETE: eliminación, errores, respuesta vacía

**Total:** Setenta tests con cien por ciento de cobertura en app inventario.

### 4. Bugfixes Identificados y Corregidos
- Endpoint GET sin validación retornaba error al solicitar producto inexistente. Se agregó validación que retorna HTTP 404.
- Endpoint PUT retornaba HTTP 200 en lugar de 404 cuando producto no existe. Se corrigió.
- Método DELETE retornaba HTTP 200 con contenido en lugar de HTTP 204 sin contenido. Se corrigió.

### 5. Documentación Profesional
Se creó archivo PASS.md documentando exhaustivamente cada test: su objetivo, intención, pasos de ejecución, por qué pasó, código completo.

### 6. Roadmap Temporal
Se creó ROADMAP.md como guía temporal para mejorar proyecto de ocho punto cinco a nueve punto cero: deployment en producción, mejora de interfaz, agregar búsqueda.

### 7. Guía de Excelencia
Se creó EXCELLENCE.md detallando cómo alcanzar nueve punto cero, nueve punto cinco y nueve punto nueve: autenticación, documentación, features avanzadas, DevOps, code quality.

---

## 📊 ESTADO ACTUAL DEL PROYECTO

**Calificación:** Siete punto cinco de diez

**Fortalezas:**
- Arquitectura sólida y separación de responsabilidades clara
- Testing exhaustivo con cobertura completa
- Documentación técnica detallada
- Bugfixes implementados
- Código que sigue estándares profesionales
- CRUD completamente funcional

**Debilidades que quedan:**
- Sin deployment en producción
- Interfaz visual aún muy básica
- Autenticación JWT no implementada en vistas
- Sin features avanzadas como dashboards o exportación

---

## 📁 ARCHIVOS CLAVE

**PASS.md:** Documentación de cada test hecho, qué verifica, por qué pasó

**ROADMAP.md:** Plan temporal para ir de ocho punto cinco a nueve puntos, con instrucciones para persona y agente

**EXCELLENCE.md:** Guía de cómo alcanzar nueve punto nueve, todas las features deseables, prioridades

**pytest.ini:** Configuración de pytest con coverage automático

**conftest.py:** Fixtures globales para tests, clientes API, datos de prueba

**factories.py:** Factory para crear instancias de ListaProducto con datos aleatorios

**test_models.py:** Tests unitarios del modelo

**test_serializers.py:** Tests unitarios del serializador

**test_views_get.py:** Tests de integración para endpoints GET

**test_views_post.py:** Tests de integración para endpoints POST

**test_views_put.py:** Tests de integración para endpoints PUT

**test_views_delete.py:** Tests de integración para endpoints DELETE

---

## 🚀 CÓMO EJECUTAR

**Inicializar backend:**
Cambiar a carpeta BACKEND, activar venv con source venv bin activate, ejecutar python manage.py runserver

**Inicializar frontend:**
Cambiar a carpeta TIENDA_FRONTED, activar venv con source venv bin activate, ejecutar reflex run

**Ejecutar todos los tests:**
Desde carpeta BACKEND activado el venv, ejecutar pytest inventario para ver todos los tests, o pytest --cov para ver coverage

**Ver cobertura visual:**
Los tests generan automáticamente reporte HTML en htmlcov index.html

---

## 📝 CONVENCIONES Y ESTÁNDARES

**Naming:** Modelos singulares, vistas APIView, métodos HTTP minúsculas, variables snake_case

**Testing:** Cada test es independiente, puede correr en cualquier orden, usa fixtures para datos compartidos

**Archivos temporales:** ROADMAP.md y otros archivos temporales están marcados en línea uno para eliminar cuando proyecto esté listo

**Documentación:** Cada archivo .md tiene propósito específico y audiencia: persona o agente

---

## 🔗 RELACIÓN CON GIT

**Rama actual:** agents-profitable-skink

**Commits recientes:**
- Implementación completa de TDD: setenta tests con cien por ciento cobertura
- Se realizaron arreglos generales, se agregó archivo REVERSE.md como instrucción general, se agregó archivo COMANDOS.txt como instructivo de inicialización
- Se agregó configuración de gitignore en raíz y frontend para excluir entornos virtuales
- Primer commit limpio

**Remoto:** GitHub en https github.com JANolazco Tienda_web3

---

## 🎓 LECCIONES APRENDIDAS

**TDD funciona:** Los tests encontraron tres bugs antes de llegar a producción

**Documentación es crucial:** PASS.md explicando cada test hace el código autoexplicativo

**Estructura importa:** Separación clara entre models, views, serializers permite escalar fácilmente

**Validación en capas:** Tests de models, serializers, y views por separado cubren todos los ángulos

---

## ⏭️ PRÓXIMOS PASOS PARA AGENTES

Si llegas nuevo a este proyecto:

1. Lee este archivo para entender contexto general
2. Lee PASS.md para entender qué tests existen y por qué
3. Lee ROADMAP.md si vas a agregar features nuevas
4. Lee EXCELLENCE.md si vas a mejorar calidad del código
5. Ejecuta los tests para verificar que todo funciona: pytest inventario
6. Explora los archivos clave mencionados arriba para entender arquitectura

---

## 🆘 PREGUNTAS COMUNES

**¿Por qué hay tantos archivos .md?**
Cada .md tiene propósito específico: PASS documenta tests, ROADMAP es plan temporal, EXCELLENCE es aspiracional, REVERSE es traza inversa, CONTEXTO es este archivo.

**¿Por qué pytest en lugar de unittest?**
pytest es más moderno, tiene mejor sintaxis, mejor fixtures, integración más fácil con plugins como coverage.

**¿Por qué Factory en lugar de fixtures duras?**
Factory genera datos aleatorios realistas, permite parametrización, descubre bugs que fixtures duras no ven.

**¿Dónde está la autenticación real?**
JWT está configurado en Django pero no protege vistas. Está en el roadmap para implementar.

**¿Puedo agregar más tests?**
Sí, sigue el mismo patrón: test primero, luego código. Usa las factories para data. Los tests nuevos deben tener coverage automático.

---

## 📞 CONTACT POINTS

**Para entender logging:** Ver conftest.py

**Para entender factories:** Ver factories.py

**Para ver tests modelos:** Ver test_models.py

**Para ver tests API:** Ver test_views_get.py, test_views_post.py, test_views_put.py, test_views_delete.py

**Para ver ejemplos de código:** Leer EXCELLENCE.md que tiene ejemplos de qué falta

---

**Este proyecto:** Educacional, enfocado en buenas prácticas, completamente testeado, listo para mejorar hacia producción.

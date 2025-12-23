# UniYoklama (QR + Geofence MVP)

Bu repo, ara raporda tarif edilen UniYoklama sisteminin (Flask REST + SQLAlchemy + JWT/RBAC + Vue 3) **QR kod ile yoklama** ve **kampüs (geofence) kontrolü** gereksinimini karşılayan, hızlıca ayağa kalkabilen bir MVP iskeletidir.

## 1) Backend Kurulum

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt

# Config dosyasını kopyala ve düzenle
cp config.example.cfg config.cfg
```

### Çalıştırma

```bash
# SQLite ile:
python run.py --config ./config.cfg

# veya FLASK ile:
flask --app wsgi:app run --debug
```

### DB oluşturma

```bash
flask --app wsgi:app init-db
```

### Demo veri (seed)

```bash
flask --app wsgi:app seed
```

Demo kullanıcılar:
- Instructor: `instructor@demo.com` / `demo1234`
- Student: `student@demo.com` / `demo1234`



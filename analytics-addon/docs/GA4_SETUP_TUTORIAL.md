# Tutorial: Setup Google Analytics 4 dengan Akun Terpisah

## Step 1: Buat Google Account Khusus

### 1.1 Buka Gmail
- URL: https://accounts.google.com/signup
- Atau langsung ke: https://mail.google.com

### 1.2 Isi Form
```
First name: Bagas
Last name: Analytics
Username: analytics@{{DOMAIN}} (atau admin@{{DOMAIN}})
Password: [strong password]
```

### 1.3 Verifikasi
- Nomor HP (untuk recovery)
- Email recovery (opsional)

### 1.4 Aktifkan 2FA (WAJIB)
1. Buka: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow steps (HP verification)

---

## Step 2: Buat Google Analytics 4 Property

### 2.1 Buka Google Analytics
- URL: https://analytics.google.com/
- Login pakai akun `analytics@{{DOMAIN}}`

### 2.2 Buat Property
1. Click **Admin** (gear icon, bottom left)
2. Click **+ Create Property**

### 2.3 Isi Property Details
```
Property name: {{DOMAIN}}
Reporting time zone: (GMT+07:00) Jakarta
Currency: Indonesian Rupiah (IDR)
```

Click **Next**

### 2.4 Business Details
```
Industry category: Technology (atau Education)
Business size: Small
```

Click **Next**

### 2.5 Business Objectives
Pilih:
- ✅ Generate leads
- ✅ Drive online sales
- ✅ Raise brand awareness
- ✅ Examine user behavior

Click **Create**

### 2.6 Accept Terms
- Accept GA Terms of Service
- Pilih negara: Indonesia

---

## Step 3: Setup Data Stream

### 3.1 Pilih Platform
Click **Web**

### 3.2 Setup Web Stream
```
Website URL: https://{{DOMAIN}}
Stream name: {{DOMAIN}}
Enhanced measurement: ✅ ON
```

### 3.3 Enhanced Measurement Settings
Pastikan semua aktif:
- ✅ Page views
- ✅ Scrolls
- ✅ Outbound clicks
- ✅ Site search
- ✅ Video engagement
- ✅ File downloads

Click **Create stream**

### 3.4 Copy Measurement ID
- Format: `G-XXXXXXXXXX`
- Simpan ini — dibutuhkan untuk install tracking code

---

## Step 4: Install Tracking Code

### Option A: WordPress (Plugin)

#### Cara 1: Google Site Kit (Recommended)
1. Login WordPress admin
2. Go to **Plugins → Add New**
3. Search "Google Site Kit"
4. Click **Install Now** → **Activate**
5. Follow setup wizard
6. Login pakai `analytics@{{DOMAIN}}`
7. Pilih property `{{DOMAIN}}`
8. Done!

#### Cara 2: MonsterInsights
1. Install plugin MonsterInsights
2. Connect dengan Google account
3. Pilih GA4 property

#### Cara 3: Manual (Header Script)
1. Go to **Appearance → Theme File Editor**
2. Edit `header.php`
3. Tambahkan kode ini di `<head>`:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

4. Ganti `G-XXXXXXXXXX` dengan Measurement ID kamu
5. Save

---

### Option B: Blogger

1. Login Blogger
2. Go to **Theme → Edit HTML**
3. Cari `<head>`
4. Tambahkan tracking code (sama seperti di atas)
5. Save

---

### Option C: Custom HTML/Static Site

Tambahkan tracking code di `<head>` setiap halaman:

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
  <!-- ... other head elements ... -->
</head>
<body>
  <!-- ... -->
</body>
</html>
```

---

## Step 5: Verifikasi Tracking

### 5.1 Realtime Report
1. Buka Google Analytics
2. Go to **Reports → Realtime**
3. Buka `https://{{DOMAIN}}` di tab baru
4. Harus muncul active users dalam 30 detik

### 5.2 Debug Mode
1. Install Chrome Extension: "Google Analytics Debugger"
2. Aktifkan extension
3. Buka blog kamu
4. Check console untuk debug info

### 5.3 GA4 DebugView
1. Go to **Admin → DebugView**
2. Add debug parameter:
   - Chrome: `?debug_mode=true`
   - Atau install GA Debugger extension
3. Events harus muncul di DebugView

---

## Step 6: Setup Google Search Console

### 6.1 Buka Search Console
- URL: https://search.google.com/search-console

### 6.2 Tambah Property
1. Click **Add property**
2. Pilih **URL prefix**
3. Masukkan: `https://{{DOMAIN}}`
4. Click **Continue**

### 6.3 Verifikasi via GA
1. Pilih **Google Analytics** sebagai verification method
2. Pastikan login pakai `analytics@{{DOMAIN}}`
3. Click **Verify**

### 6.4 Submit Sitemap
1. Go to **Sitemaps**
2. Masukkan: `sitemap.xml` (atau path sitemap kamu)
3. Click **Submit**

---

## Step 7: Share Access (Kalau Butuh Tim)

### 7.1 Tambah User
1. Buka Google Analytics
2. Go to **Admin**
3. Di kolom **Account**, click **Account Access Management**
4. Click **+** (add)
5. Masukkan email tim
6. Pilih role:
   - **Viewer** —只看数据
   - **Editor** — bisa edit settings
   - **Administrator** — full access

### 7.2 Tambah ke Search Console
1. Buka Search Console
2. Go to **Settings → Users and permissions**
3. Click **Add user**
4. Masukkan email + role

---

## Troubleshooting

### Tracking tidak muncul di Realtime
1. Cek Measurement ID benar
2. Clear browser cache
3. Disable ad blockers
4. Tunggu 24-48 jam untuk data historis

### Error "No data received"
1. Pastikan kode ada di `<head>`, bukan `<body>`
2. Cek console browser untuk errors
3. Verify pakai GA Debugger extension

### Data tidak akurat
1. Filter internal traffic:
   - Go to **Admin → Data Streams → Configure tag settings**
   - Add internal traffic rule
2. Exclude自己的 IP

---

## Best Practices

### 1. Jangan Track Diri Sendiri
Buat filter untuk exclude IP kantor/rumah:
1. Go to **Admin → Data Streams**
2. Click **Configure tag settings**
3. Click **Define internal traffic**
4. Add rule untuk IP kamu

### 2. Setup Conversions
1. Go to **Admin → Events**
2. Toggle "Mark as conversion" untuk event penting:
   - `page_view` (default)
   - `form_submit`
   - `scroll` (optional)

### 3. Buat Custom Reports
1. Go to **Explore**
2. Buat custom report sesuai kebutuhan
3. Save sebagai template

---

## Checklist Setup

- [ ] Google Account created (`analytics@{{DOMAIN}}`)
- [ ] 2FA activated
- [ ] GA4 property created
- [ ] Web data stream configured
- [ ] Measurement ID saved (`G-XXXXXXXXXX`)
- [ ] Tracking code installed di blog
- [ ] Realtime report verified
- [ ] Search Console connected
- [ ] Sitemap submitted
- [ ] Internal traffic filtered
- [ ] Conversions configured
- [ ] Documentation saved

---

## Credentials Template

Simpan di tempat aman:

```
Platform: Google Analytics 4
Account: analytics@{{DOMAIN}}
Password: [REDACTED]
2FA: Enabled
Property: {{DOMAIN}}
Measurement ID: G-XXXXXXXXXX
Search Console: https://search.google.com/search-console
```

---

**Status:** Draft untuk Publisher
**Author:** Blog Orchestrator
**Date:** 2026-06-17
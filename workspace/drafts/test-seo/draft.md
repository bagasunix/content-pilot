---
title: "Cara Install Redis di Ubuntu 24.04"
meta_description: "Panduan lengkap cara install Redis di Ubuntu 24.04. Mulai dari apt, source, hingga Docker. Cocok untuk pemula dan developer."
slug: "cara-install-redis-ubuntu-2404"
keywords: "install redis ubuntu, redis tutorial"
---

# Cara Install Redis di Ubuntu 24.04

Redis adalah in-memory data store yang sering digunakan sebagai cache, message broker, dan database. Artikel ini akan membahas cara install Redis di Ubuntu 24.04.

## Kenapa Pakai Redis?

Redis memiliki beberapa kelebihan dibandingkan database lain:

- Kecepatan tinggi (microsecond latency)
- Mendukung berbagai data structures
- Mudah di-setup dan dikonfigurasi

## Cara Install via APT

```bash
sudo -S -p '' apt update
sudo -S -p '' apt install redis-server
```

Setelah install, Redis akan otomatis running. Cek statusnya:

```bash
sudo -S -p '' systemctl status redis-server
```

## Konfigurasi

Edit file `/etc/redis/redis.conf` untuk mengubah port atau password.

## Kesimpulan

Redis adalah pilihan yang bagus untuk caching. Dengan panduan ini, kamu sudah bisa install Redis di Ubuntu 24.04.

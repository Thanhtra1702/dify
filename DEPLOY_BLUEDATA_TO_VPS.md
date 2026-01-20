# Hướng dẫn Deploy BlueData Branding lên VPS

## Tổng quan
Hướng dẫn này giúp bạn cập nhật Dify trên VPS để hiển thị "Powered by BlueData" thay vì "Powered by Dify", mà không ảnh hưởng đến dữ liệu và cấu hình hiện tại.

## Bước 1: Backup dữ liệu (Quan trọng!)

```bash
# SSH vào VPS
ssh user@your-vps-ip

# Backup database
cd /path/to/dify
docker exec docker-db_postgres-1 pg_dump -U postgres dify > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup volumes
sudo tar -czf dify_volumes_backup_$(date +%Y%m%d_%H%M%S).tar.gz ./volumes/
```

## Bước 2: Pull code mới từ repository

```bash
# Di chuyển đến thư mục Dify
cd /path/to/dify

# Stash các thay đổi local (nếu có)
git stash

# Pull code mới
git pull origin main

# Kiểm tra xem file đã được cập nhật chưa
cat web/app/components/base/logo/dify-logo.tsx
# Bạn sẽ thấy "BlueData" trong file này
```

## Bước 3: Build Docker image mới

```bash
# Build web image với code mới
cd web
docker build -t dify-web-bluedata:latest .

# Quay lại thư mục gốc
cd ..
```

**Lưu ý**: Quá trình build có thể mất 5-10 phút tùy thuộc vào cấu hình VPS.

## Bước 4: Cập nhật container web

```bash
# Dừng và xóa container web cũ
docker stop docker-web-1
docker rm docker-web-1

# Lấy thông tin cấu hình từ docker-compose
cd docker

# Chạy container mới với image vừa build
docker run -d \
  --name docker-web-1 \
  --network docker_default \
  --network-alias web \
  -e CONSOLE_API_URL=${CONSOLE_API_URL:-} \
  -e APP_API_URL=${APP_API_URL:-} \
  -e AMPLITUDE_API_KEY=${AMPLITUDE_API_KEY:-} \
  -e NEXT_PUBLIC_COOKIE_DOMAIN=${NEXT_PUBLIC_COOKIE_DOMAIN:-} \
  -e SENTRY_DSN=${WEB_SENTRY_DSN:-} \
  -e NEXT_TELEMETRY_DISABLED=${NEXT_TELEMETRY_DISABLED:-0} \
  -e TEXT_GENERATION_TIMEOUT_MS=${TEXT_GENERATION_TIMEOUT_MS:-60000} \
  -e CSP_WHITELIST=${CSP_WHITELIST:-} \
  -e ALLOW_EMBED=${ALLOW_EMBED:-false} \
  -e ALLOW_UNSAFE_DATA_SCHEME=${ALLOW_UNSAFE_DATA_SCHEME:-false} \
  -e MARKETPLACE_API_URL=${MARKETPLACE_API_URL:-https://marketplace.dify.ai} \
  -e MARKETPLACE_URL=${MARKETPLACE_URL:-https://marketplace.dify.ai} \
  --restart always \
  dify-web-bluedata:latest
```

## Bước 5: Kiểm tra

```bash
# Kiểm tra container đang chạy
docker ps | grep docker-web-1

# Xem logs để đảm bảo không có lỗi
docker logs docker-web-1 --tail 50

# Kiểm tra trên trình duyệt
# Truy cập vào domain của bạn và kiểm tra chatbot
# Bạn sẽ thấy "Powered by BlueData" ở phía dưới chatbot
```

## Bước 6: Dọn dẹp (Tùy chọn)

```bash
# Xóa image cũ để tiết kiệm dung lượng
docker images | grep dify-web
docker rmi langgenius/dify-web:1.11.2
```

## Rollback (Nếu có vấn đề)

Nếu gặp vấn đề, bạn có thể rollback về phiên bản cũ:

```bash
# Dừng container mới
docker stop docker-web-1
docker rm docker-web-1

# Chạy lại container với image gốc
docker run -d \
  --name docker-web-1 \
  --network docker_default \
  --network-alias web \
  [các env variables giống như trên] \
  langgenius/dify-web:1.11.2
```

## Cách đơn giản hơn (Khuyến nghị)

Nếu bạn muốn cách đơn giản hơn, tạo file `docker-compose.override.yml`:

```yaml
services:
  web:
    build:
      context: ../web
      dockerfile: Dockerfile
    image: dify-web-bluedata:latest
```

Sau đó chỉ cần chạy:

```bash
cd docker
docker compose build web
docker compose up -d web
```

## Lưu ý quan trọng

1. **Backup trước khi thực hiện**: Luôn backup database và volumes trước khi update
2. **Downtime**: Quá trình update sẽ có downtime khoảng 5-10 phút
3. **Kiểm tra kỹ**: Sau khi update, kiểm tra kỹ các chức năng chính
4. **Image size**: Image mới sẽ chiếm thêm khoảng 500MB-1GB dung lượng

## Troubleshooting

### Container không khởi động
```bash
# Xem logs chi tiết
docker logs docker-web-1

# Kiểm tra network
docker network inspect docker_default
```

### 502 Bad Gateway
```bash
# Kiểm tra container web có đang chạy không
docker ps | grep docker-web-1

# Restart nginx
docker restart docker-nginx-1
```

### Không thấy thay đổi
```bash
# Clear browser cache
# Hoặc mở Incognito mode để kiểm tra
```

## Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Logs của container: `docker logs docker-web-1`
2. Logs của nginx: `docker logs docker-nginx-1`
3. Network connectivity: `docker network inspect docker_default`

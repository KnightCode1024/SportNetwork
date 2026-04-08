# TODO — Implemented vs Not Implemented Endpoints

## Users (`/api/v1/users`)

- [x] `POST /register` — Регистрация пользователя
- [x] `GET /verify-email` — Подтверждение email
- [x] `POST /login` — Вход в аккаунт
- [ ] `POST /refresh` — Обновление access/refresh токенов
- [ ] `POST /check-code` — Проверка кода 2FA
- [ ] `GET /resend-code` — Повторная отправка кода 2FA
- [x] `GET /me` — Получение текущего пользователя (через `AuthProvider`)
- [x] `POST /reset-password` — Сброс пароля
- [ ] `GET /logout` - блэк лист токенов

## Profile (`/api/v1/profile`)
- [ ] `GET /` — Получение профиля
- [ ] `PATCH /` — Обновление профиля
- [ ] `POST /avatar` — Загрузка аватара
- [ ] `DELETE /avatar` — Удаление аватара

## Settings (`/api/v1/settings`)
(Провайдер уведомлений, 2fa)
- [ ] `GET /settings` — Получение настроек
- [ ] `PATCH /settings` — Обновление настроек
- [ ] `POST /settings` — Создание настроек
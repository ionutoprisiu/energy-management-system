# Postman (minimal)

1. Import:
   - `postman/collections/ems-auth-user.postman_collection.json`
   - `postman/environments/local.postman_environment.json`
2. Select environment `Local EMS`.
3. Run requests in this order:
   - `01 Auth - Register Admin`
   - `02 Auth - Login Admin` (sets `ADMIN_TOKEN`)
   - `03 Users - Create Admin Profile`
   - `04 Auth - Register Client`
   - `05 Users - Create Client Profile` (sets `USER_ID`)
   - `06 Auth - Login Client` (sets `CLIENT_TOKEN`)
   - `07 Users - Get All`
   - `08 Users - Get Client By ID`
   - `09 Devices - Create` (sets `DEVICE_ID`)
   - `10 Devices - Get All`
   - `11 Devices - Assign To Client`
   - `12 Devices - My Devices`
   - `13 Devices - Unassign`
   - `14 Devices - Delete`

For the cleanest run, start from an empty database volume:

```bash
docker compose down -v
docker compose up --build
```

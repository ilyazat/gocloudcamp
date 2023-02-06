#!/bin/ash
sleep 3
echo "Testing started"
echo "Running curls"

curl -d "@data.json" -H "Content-Type: application/json" -X POST http://api:8080/config > output
echo >> output
curl http://api:8080/config?service=managed-k8s >> output
echo >> output
curl -X PUT -d "@update.json" -H 'accept: application/json' -H "Content-Type: application/json" http://api:8080/config >> output
echo >> output
curl -X 'GET' 'http://api:8080/config?service=managed-k8s&version=1' -H 'accept: application/json' >> output
echo >> output
curl -X 'GET' 'http://api:8080/config?service=managed-k8s&version=2' -H 'accept: application/json' >> output
echo >> output
curl -X 'PUT' 'http://api:8080/config/add_app?service=managed-k8s&app_label=nginx' -H 'accept: application/json' >> output
echo >> output
curl -X 'DELETE' 'http://api:8080/config?service=managed-k8s' -H 'accept: application/json' >> output
echo >> output
curl -X 'PUT' 'http://api:8080/configremove_app?service=managed-k8s&app_label=nginx' -H 'accept: application/json' >> output
echo >> output
curl -X 'DELETE' 'http://api:8080/config?service=managed-k8s' -H 'accept: application/json' >> output

echo "output:"
echo
cat output
diff answer output

if [ $? -ne 0 ]; then
echo "Testing has failed, exiting with code 1"
exit 1
else
echo
echo "Testing has been done successfully"
fi

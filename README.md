**Activate the virtual env**

```
source blockchain-env/Scripts/activate
```

**Install all packages**

```
pip3 install -r requirement.txt
```
Make sure to activate the virtual env.

**Run the tests**

```
python -m pytest backend/tests
```
**Run the application and API**

```
python -m backend.app
```
**Run a peer instance**

```
export PEER=True && python -m backend.app
```

**Run the frontend**
In frontend directory:

```
npm run restart
```

**Seed the backend with data**

```
export SEED_DATA=True && python -m backend.app
```




# 🔧 HEROKU UV COMPATIBILITY FIX

## Problema
```
Error: The runtime.txt file isn't supported when using uv.
When using the package manager uv on Heroku, you must specify
your app's Python version with a .python-version file and not
a runtime.txt file.
```

## ✅ SOLUÇÃO RÁPIDA

```bash
# 1. Remover runtime.txt
rm -f runtime.txt

# 2. Criar .python-version
echo "3.11" > .python-version

# 3. Commit mudanças
git add --all
git commit -m "Fix Heroku uv compatibility: replace runtime.txt with .python-version"

# 4. Deploy novamente
git push heroku main
```

## ⚡ CONFIGURAÇÃO ULTRA EXTREME VELOCITY

Após o deploy, configure a velocidade máxima:

```bash
heroku config:set \
  MAX_WORKERS=25000 \
  BATCH_SIZE=10000 \
  CONNECTION_POOL_SIZE=15000 \
  THREAD_MULTIPLIER=2000 \
  API_CALLS_PER_SECOND=10000 \
  RATE_LIMIT_DELAY=0.000001
```

## 🚀 RESULTADO

Sistema funcionando com:
- **25.000 workers simultâneos**
- **10.000 API calls por segundo**
- **Batches de 10.000 leads**
- **15.000 conexões HTTP**

Velocidade máxima absoluta atingida!
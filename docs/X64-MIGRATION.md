# Aegis — migração para builder Linux x86-64

## Estado transferido

O repositório Aegis está preparado para Chromium `151.0.7922.173`. A série versionada em `patches/series` contém, nesta ordem:

1. `0001-privacy-defaults-background-prediction.patch`;
2. `0002-tracking-url-utils.patch`;
3. `0003-anonymous-egress-gate.patch`.

Os três patches passaram aplicação isolada e ordenada com `git am --3way` contra arquivos exatos da tag M151. Isso não substitui compilação. Os testes C++, browser tests e leak tests continuam `BLOCKED` até execução no builder.

## Requisitos do builder

Use uma máquina nova com:

- Ubuntu ou Debian Linux x86-64 nativo;
- 16 GiB de RAM no mínimo; 32 GiB recomendados;
- pelo menos 200 GiB livres em SSD;
- acesso à internet para Gitiles, depot_tools, gclient e pacotes apt;
- usuário com root ou `sudo` para dependências;
- filesystem sensível a maiúsculas/minúsculas.

VM x86-64 é aceitável se oferecer os recursos acima. Não use o ARM64/PRoot atual para tentar a compilação completa.

## 1. Transferir o repositório

Método preferido, quando houver remote Git:

```bash
git clone <URL-DO-REPOSITORIO-AEGIS> aegis-browser
cd aegis-browser
git checkout main
git status --short
```

`git status --short` deve ficar vazio. Se ainda não existir remote, crie um bundle na máquina de origem e copie-o:

```bash
cd /root/browser
git bundle create /tmp/aegis-browser.bundle --all
scp /tmp/aegis-browser.bundle usuario@builder:/tmp/
```

No builder:

```bash
git clone /tmp/aegis-browser.bundle aegis-browser
cd aegis-browser
git checkout main
git status --short
git log --oneline -10
```

Confirme que os commits `440f76e`, `c6e2fbd`, `bd076d3` e `4897fd9` aparecem. Não copie `src/`, `depot_tools/`, `build/work/`, `out/` ou caches; eles são recriados.

## 2. Verificar o conteúdo antes do setup

```bash
cd aegis-browser
python3 -m unittest discover -v
scripts/verify_security_flags.sh
sed -n '/^[^#[:space:]]/p' patches/series
```

A série deve listar exatamente os três patches na ordem documentada acima.

## 3. Preparar o builder com um comando

O script instala/verifica dependências, obtém depot_tools, busca a versão fixada, sincroniza gclient, instala as dependências oficiais do Chromium, aplica a série, executa `gn gen` e faz um dry-run Ninja:

```bash
scripts/setup-x64-builder.sh
```

Checkout gerado por padrão:

```text
build/work/x64-checkout/src
```

Um symlink ignorado pelo Git é criado em `src`, e a saída GN fica em:

```text
src/out/Aegis
```

O setup não inicia a compilação pesada por padrão. Para fazer setup e iniciar o build na mesma execução:

```bash
scripts/setup-x64-builder.sh --build
```

Use `--skip-system-deps` apenas em uma imagem que já tenha todas as dependências apt e Chromium instaladas:

```bash
scripts/setup-x64-builder.sh --skip-system-deps
```

## 4. Primeira compilação

Após o setup normal terminar com `PASS`:

```bash
export PATH="$PWD/depot_tools:$PATH"
autoninja -C src/out/Aegis chrome
```

Não use `--no-sandbox`, `--ignore-certificate-errors` nem desative Site Isolation/TLS para contornar erros.

## 5. Testes nativos iniciais

Compile o target de testes e execute os filtros dos 11 testes C++ adicionados:

```bash
autoninja -C src/out/Aegis unit_tests
src/out/Aegis/unit_tests \
  --gtest_filter='TrackingUrlUtilsTest.*:AnonymousEgressGateTest.*'
```

Depois execute:

```bash
scripts/test_all.sh
scripts/verify_security_flags.sh
git -C src diff --check
```

Os patches de defaults também exigem testes de perfil/browser: confirmar background mode `false`, network prediction `kDisabled`, persistência de overrides do usuário e ausência de regressões em updates, Safe Browsing, sandbox, Site Isolation e TLS.

## 6. Trabalho permitido após a primeira build

Somente depois de o Chromium e os testes nativos compilarem:

1. corrigir erros C++/GN dos patches existentes em commits separados;
2. integrar `StripTrackingParameters()` ao fluxo de navegação, com browser tests de redirects, histórico, referrer, downloads, POST e garantia de que a URL suja não escapou;
3. conectar `AnonymousEgressGate` ao Network Service, `NetworkContext`, DNS e socket factories;
4. implementar revogação de sockets/contextos e restart bloqueado;
5. executar browser tests e captura externa de TCP/UDP/DNS/DoH/WebRTC;
6. só então trabalhar nas superfícies renderer-level de anti-fingerprint.

Até concluir socket integration e leak tests, o gate é apenas uma fundação e Anonymous não possui garantia nativa completa. Para anonimato de alto risco, use Tor Browser.

## 7. Workflow GitHub Actions

`.github/workflows/chromium-x64.yml` foi verificado estaticamente. Ele:

- exige runner self-hosted com labels `linux`, `x64`, `chromium-builder`;
- exige pelo menos 200 GiB livres;
- executa bootstrap, `scripts/apply_patches.sh`, build x86-64 e suíte host-capable;
- possui timeout de 720 minutos.

O workflow faz build completo. O novo `scripts/setup-x64-builder.sh` é o caminho recomendado para preparar e diagnosticar interativamente uma máquina nova antes de registrar o runner.

## 8. Recuperação de falhas

Se um patch falhar:

```bash
cd build/work/x64-checkout/src
git am --show-current-patch=diff
git status
git am --abort
```

Registre o erro completo. Corrija o patch no repositório Aegis, regenere com `git format-patch`, teste novamente numa árvore limpa e faça um novo commit. Não force aplicação parcial.

Se `gclient sync` falhar por transporte, repita o mesmo comando no diretório de trabalho:

```bash
cd build/work/x64-checkout
gclient sync --with_branch_heads --with_tags --no-history
```

Se o build falhar, preserve a primeira mensagem de compilação relevante e o comando Ninja. Não trate `git am --3way` como prova de compilação.

## 9. Critério de migração concluída

A migração estará concluída somente quando houver evidência real de:

- checkout exato do Chromium `151.0.7922.173`;
- três patches aplicados na ordem;
- `gn gen` concluído;
- `autoninja ... chrome` concluído;
- 11 testes C++ executados;
- suíte Aegis e scanner de segurança verdes;
- worktree Aegis limpa com correções versionadas.

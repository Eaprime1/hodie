# Gravity Repo Architecture - Multi-Core System

**Concept:** Repository of gravity cores, each <1GB, spawning new cores as needed

---

## Structure

```
gravity-cores/ (GitHub repo)
│
├── cores/
│   ├── gravity_core_v1.0_SEED.zip      (1.9 GB - split needed)
│   ├── gravity_core_v1.1_alpha.zip     (<1 GB)
│   ├── gravity_core_v1.2_beta.zip      (<1 GB)
│   └── gravity_core_v2.0_gamma.zip     (<1 GB)
│
├── manifests/
│   ├── core_v1.0_manifest.json
│   ├── core_v1.1_manifest.json
│   └── unified_manifest.json           (all cores combined)
│
├── docs/
│   ├── GRAVITY_CORE_MISSION.md
│   ├── README.md
│   └── USAGE.md
│
└── tools/
    ├── core_spawn.py                    (creates new core when limit hit)
    ├── core_query.py                    (query across all cores)
    └── core_merge.py                    (combine manifests)
```

---

## Spawning Strategy

**Trigger:** When approaching 1GB compressed
**Action:** Spawn new core with seed from parent

```python
def spawn_new_core(current_core, new_duplicates):
    """
    Spawn next gravity core when size limit approached

    Strategy:
    1. Check current core size
    2. If >900 MB, spawn new core
    3. Carry seed from parent (top gravity docs)
    4. New core inherits lineage
    """
    if get_core_size(current_core) > 900 * 1024 * 1024:  # 900 MB
        next_version = increment_version(current_core)
        seed_docs = extract_top_gravity(current_core, count=100)
        create_core(next_version, new_duplicates, seed=seed_docs)
```

---

## Benefits

- ✅ Each core <1GB (GitHub friendly)
- ✅ Spawn infinitely as data grows
- ✅ Each core has lineage/seed
- ✅ Query across all cores
- ✅ Distribute individually or combined
- ✅ Flag system tracks spawning

---

## Initial Split

Current: 1.9 GB → Split to 2 cores:
- gravity_core_v1.0_alpha.zip (~950 MB)
- gravity_core_v1.0_beta.zip  (~950 MB)

Both released, both queryable, both track gravity.

€(gravity_repo_arch)

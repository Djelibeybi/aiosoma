# Changelog

<!--next-version-placeholder-->

## v1.1.5 (2023-03-15)
### Fix
* **deps:** Update dependency rich to v13.3.2 ([`1d2e96f`](https://github.com/Djelibeybi/aiosoma/commit/1d2e96f9121ab81db1539daad5cbd25a29478bb2))

## v1.1.4 (2023-01-01)
### Fix
* **deps:** Update dependency rich to v13 ([`35d07b5`](https://github.com/Djelibeybi/aiosoma/commit/35d07b543c66354ed02efa772e697f8a4957e0dc))

## v1.1.3 (2022-12-19)
### Fix
* Make get_light_level fetch a value before being rate limited ([`7975cd9`](https://github.com/Djelibeybi/aiosoma/commit/7975cd93813a0810e8b53da59bbac01c7b0b7f54))

## v1.1.2 (2022-12-18)
### Fix
* Revert list_devices() back to a set of tuples ([`015ae83`](https://github.com/Djelibeybi/aiosoma/commit/015ae83726600acf640c7d7c1f3364dc6e82f53f))

## v1.1.1 (2022-12-18)
### Fix
* List_devices() no longer returns SomaShade objects ([`2a70db4`](https://github.com/Djelibeybi/aiosoma/commit/2a70db4759c809a766eac74d5c86e0a4f9011dcf))

## v1.1.0 (2022-12-18)
### Feature
* Add version property to the SomaConnect class ([`7e1d0dc`](https://github.com/Djelibeybi/aiosoma/commit/7e1d0dc1bfa31185789fa7a8d40245d2cca97e2d))

## v1.0.0 (2022-12-18)
### Feature
* Limit calls to get_light_level to once per 10 minutes ([`08dac2b`](https://github.com/Djelibeybi/aiosoma/commit/08dac2b5c49690cb858f3b0a544117bfb11a8c19))

### Fix
* Resolve type issues and improve code coverage by tests ([`55930b5`](https://github.com/Djelibeybi/aiosoma/commit/55930b51353fadd8cd23ffb7afef0dbc903344b1))

### Breaking
* class names have changed as follows: ([`08dac2b`](https://github.com/Djelibeybi/aiosoma/commit/08dac2b5c49690cb858f3b0a544117bfb11a8c19))

## v0.2.2 (2022-12-17)
### Fix
* Downgrade aiohttp to suitable version for Home Assistant ([`b02a602`](https://github.com/Djelibeybi/aiosoma/commit/b02a602e6f9d29bbe7680bd304f838e0164e4b3c))

### Documentation
* Update the project name and usage docs for readthedocs ([`231a3f4`](https://github.com/Djelibeybi/aiosoma/commit/231a3f404b660cad20c0e1be5da7858c68b036ef))
* Fix formatting of aiosoma (again) ([`6a0fcb4`](https://github.com/Djelibeybi/aiosoma/commit/6a0fcb4785dd01699f852d68513a135d74915483))
* Update the contribution guide ([`7987ffc`](https://github.com/Djelibeybi/aiosoma/commit/7987ffc4fb80b6d0a35df66ddb1932e8588ca913))

## v0.2.1 (2022-12-16)
### Fix
* Remove debug print line ([`7c759f0`](https://github.com/Djelibeybi/aiosoma/commit/7c759f0589444fa641dafa81c7eb7561ecbde249))

## v0.2.0 (2022-12-16)
### Feature
* Add 'soma' command-line utility to control shades ([`52f73e2`](https://github.com/Djelibeybi/aiosoma/commit/52f73e2710d1c54523d5416fc1653382db709d72))
* Add all available control and info options ([`200ba20`](https://github.com/Djelibeybi/aiosoma/commit/200ba2091a32b2d309935a87f704027b91e3093c))
* Enable open_upwards, morning_mode and get_light_level ([`9801bda`](https://github.com/Djelibeybi/aiosoma/commit/9801bda94c03909fd00683dd9b94dd20acb4c787))

### Documentation
* Update URL to build status badge ([`52f1423`](https://github.com/Djelibeybi/aiosoma/commit/52f1423ece3d6e6008cc15cfde3a705a73a195cc))
* Fix the formatting of AioSoma in the docs ([`16f17b6`](https://github.com/Djelibeybi/aiosoma/commit/16f17b6e09f0ecd1642fde6c83e3a56e7c2ecad0))
* Update .all-contributorsrc [skip ci] ([`f04bd3e`](https://github.com/Djelibeybi/aiosoma/commit/f04bd3e43ea4151d9f59e5e0b257f173f3b7b3dd))
* Update README.md [skip ci] ([`84b0c23`](https://github.com/Djelibeybi/aiosoma/commit/84b0c23051e4efce8e4537d6cdd76e9e313fa2c1))

## v0.1.0 (2022-12-15)
### Feature
* Initial working version of aiosoma with tests ([#1](https://github.com/Djelibeybi/aiosoma/issues/1)) ([`9ceeb0a`](https://github.com/Djelibeybi/aiosoma/commit/9ceeb0a64b836944ee305885be832857607ac12b))

### Documentation
* Update docs to use aiosoma ([`049bd0c`](https://github.com/Djelibeybi/aiosoma/commit/049bd0cc6604ee9e801beb3391f535d2cbd93f9e))

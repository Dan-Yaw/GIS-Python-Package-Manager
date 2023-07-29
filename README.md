# GIS Python Package Manager

Use ArcGIS Online or Portal for ArcGIS to manage your Python packages. Rather then using pip, you can use this tool. 

## Usage

### Publicly available packages on ArcGIS Online

```shell
gpip install edfd95f15c3746149d940dc2ff5e48ad
```

### Packages on your Portal

```shell
gpip install edfd95f15c3746149d940dc2ff5e48ad --portal https://myportal.domain.com/portal
```

### Authentication

```shell
gpip install edfd95f15c3746149d940dc2ff5e48ad --portal https://myportal.domain.com/portal --username myusername --password mypassword
```

### Advanced Authentication

Use the argument --gis to pass in a dictionary directly to the ArcGIS API's gis.GIS() constructor. This allows you to use the ArcGIS API for Python's advanced authentication options. See the [ArcGIS API for Python documentation](https://developers.arcgis.com/python/guide/working-with-different-authentication-schemes/#Using-the-built-in-identity-handlers) for more information.

```shell
gpip install edfd95f15c3746149d940dc2ff5e48ad --gis '{"username":"myusername","password":"mypassword","client_id":"myclientid","client_secret":"myclientsecret"}'
```


from string import Template

# DB Constants
DB_TIMEOUT_IN_MS = 30000
DB_CONN_STRING = "mongodb://admin:password@mongo:27017/"

# URLs
GET_TOKEN_URL = "https://public-apis-api.herokuapp.com/api/v1/auth/token"
GET_DATA_FOR_CATEGORY_URL = Template("https://public-apis-api.herokuapp.com/api/v1/apis/entry?page=$page&category=$category")
GET_ALL_CATEGORIES_URL = Template("https://public-apis-api.herokuapp.com/api/v1/apis/categories?page=$page")


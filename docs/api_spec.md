
# API Specifications (Planning)

## Endpoint

    https://api.ink.keys.jp/

## APIs

### Obtain Token

~~~
POST /token
~~~

#### Arguments

~~~
{
    "auth": {
        "username": "sampleuser",
        "password": "samplepassword"
    },
}
~~~

#### Response

~~~
{
    "token": {
        "id": "hogehogehogehogehogehoge",
        "issued_at": ***,
        "expired_at": ***,
    }
}

~~~


### Release token

~~~
DELETE /token
~~~

#### Arguments

#### Response


### (APIs' have not writen yet...)

~~~
GET /boxes
POST /boxes
GET /cards
POST /cards
GET /cards/:card_id/records
POST /cards/:card_id/records
~~~

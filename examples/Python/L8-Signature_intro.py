from solders.signature import Signature

sig = Signature.from_string("3yv6g4XCKScNNQU7pWyFbLUs8EksfgUHz9pPAEqD5VqdASq95yLz3LkETpYzAifwBA2JeJsqYsAdUyqj5JxoLScR")
print("Строка:", str(sig))
print("Длина байт:", len(bytes(sig)))

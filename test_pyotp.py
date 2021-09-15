import pyotp
import time

# totp = pyotp.TOTP('base32secret3232')
# print(totp.now())   # Get OTP

# print(totp.verify("123456"))    # Verify OTP
# print(totp.verify(totp.now()))    # Verify OTP

# print(pyotp.random_base32())    # generating random PyOTP secret keys
# print(pyotp.random_hex())       # returns a 32-character hex-encoded secret

i = 1
while True:
    totp = pyotp.TOTP('G76ECGOP5FUH2YQ5YEF7ZDZQZHSBK6AK', interval=10)
    print(totp.provisioning_uri(name="testing"))
    print(i, totp.now())   # Get OTP
    i += 1
    time.sleep(1)

# print(pyotp.random_base32())    # G76ECGOP5FUH2YQ5YEF7ZDZQZHSBK6AK
# print(pyotp.totp.TOTP('G76ECGOP5FUH2YQ5YEF7ZDZQZHSBK6AK').provisioning_uri(name='852 12345678', issuer_name='QuantRaiser'))   # otpauth://totp/QuantRaiser:852%2012345678?secret=G76ECGOP5FUH2YQ5YEF7ZDZQZHSBK6AK&issuer=QuantRaiser

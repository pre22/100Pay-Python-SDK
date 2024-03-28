import random
import requests
import datetime

'''
This is a Python SDK for 100Pay

'''

generated_slugs = []

def generate_unique_slug():
    '''Generates Unique Slug'''
    today = str(datetime.date.today())
    slug = "{}{}".format(''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)), today.replace("-", ""))

    
    if len(generated_slugs) == 10:
        generated_slugs.clear()
    
    elif len(generated_slugs) != 10:
        counter = 0

        # Check if the slug already exists in the list
        while slug in generated_slugs:
            new_slug = "{}{}".format(''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)), today.replace("-", ""))
            slug = new_slug
            counter += 1


    # Add the new slug to the list
    generated_slugs.append(slug)

    return slug


def generate_ref_ID(business_name):
    '''
    Generate Ref ID for Transaction Using their Business Name
    '''
    result = "{}-{}".format(business_name.upper(),''.join(random.choices('0123456789', k=6)))
    return result


class PaymentGateway():
    '''
    100Pay Payment Gateway Class

    Generates Payment Charge Link 

    Verify Transactions using PaymentID

    Note: CallBack URL Must be start with https://
    '''

    def __init__(self):
        self.url = "https://api.100pay.co/api/v1/pay/charge"
        self.business_name = None
        self.callback_url = None
        self.APIKEY = None
        self.pricing_type = "fixed_or_partial_price"
        self.charge_source = "api"

        # Customer Section 
        self.user_id = None
        self.user_fullname = None
        self.user_phone = None
        self.user_email = None
        self.ref_id = None

        # Billing Section 
        self.country = "NG"
        self.currency = "NGN" # Ensure you use the appropriate currency symbol
        self.amount = 0
        self.description = 'Product/Service Payment'
        self.vat = 0



    def generate_payment_link(self, *args, **kwargs):
            '''
            Generates Payment Charge Link
            '''
        
            payload = {
                "ref_id": self.ref_id,
                "customer": {
                    "user_id": self.user_id, # From your DataBase
                    "name": self.user_fullname,
                    "phone": self.user_phone,
                    "email": self.user_email
                },
                "billing": {
                    "description": self.description,
                    "amount": float(self.amount),  # Converted to float
                    "country": self.country,
                    "currency": self.currency,
                    "vat": float(self.vat),  # Converted string to integer
                    "pricing_type": self.pricing_type
                },
                "metadata": {
                    "is_approved": True  # Converted string to boolean
                },
                "call_back_url": self.callback_url,
                "userId": generate_unique_slug(), # For Identifying the current user you're generating the payment charge for
                "charge_source": self.charge_source
            }

            headers = {
                'api-key': self.APIKEY
            }

            try:
                response = requests.post(self.url, headers=headers, json=payload)
                
            
            except requests.exceptions.ReadTimeout:
                return {"Info": "Request Timeout. Please try again or contact customer support", "status": 408}
            
            except Exception as e:
                return {"error": f"{e}", "status": 400}
            
            if response.status_code == 200:

                data = response.json()

                return {'message': data['hosted_url'], "status": 200}

            elif response.status_code != 200:
                return {'message': response.text, "status": 400}


    def verify_transactions_via_paymentID(self, payment_ID):
        '''
        Verify Transactions using PaymentID
        '''
        current_url = f"https://api.100pay.co/api/v1/pay/crypto/payment/{payment_ID}"
        
        headers = {
            'api-key': self.APIKEY
        }

        try:
            response = requests.post(current_url, headers=headers, json={})
            
        
        except requests.exceptions.ReadTimeout:
            return {"Info": "Request Timeout. Please try again or contact customer support", "status": 408}
        
        except Exception as e:
            return {"error": f"{e}", "status": 400}
        
        if response.status_code == 200:

            data = response.json()

            return {'message': data, "status": 200}

        elif response.status_code != 200:
            return {'message': response.text, "status": 400}








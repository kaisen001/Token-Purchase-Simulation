from flask import Flask, request, jsonify
import oracledb

####################################################
#  
#  description :
#  author :
#  email ;
#
####################################################

# Oracle database connection
username = 'scott'
connection_string = 'hostname:port/servicename'
password = 'mot de passe'

# Instantiate Flask service
app = Flask(__name__)

@app.route('/amount_simulation', methods=['POST'])
def amount_simulation():
    data = request.get_json()
    meter_number = data.get('meter_number')
    amount = data.get('amount')

    # Connect to db and run a query
    with oracledb.connect(user=username, password=password, dsn=connection_string) as connection:
        with connection.cursor() as cursor:
            sql = """select sysdate from dual"""
            cursor.execute(sql)
            data = cursor.fetchone()

    if not data:
        return jsonify({"error": "Meter not found"}), 404

    # Function to simulate
    result = calculate_kw(amount)

    return jsonify({
        "meter": meter_number,
        "amount": amount,
        "energy": result['energy'],
        "vat": result['vat'],
        "debts": result['debts'],
    })

@app.route('/energy_simulation', methods=['POST'])
def energy_simulation():
    data = request.get_json()
    meter_number = data.get('meter_number')
    energy = data.get('energy')

    # TODO: upgrade this part of code to be similar to the amount simulation
    with oracledb.connect(user=username, password=password, dsn=connection_string) as connection:
        with connection.cursor() as cursor:
            sql = """SELECT meter_number, debts FROM meters WHERE meter_number = :meter_number"""
            cursor.execute(sql [meter_number])
            data = cursor.fetchone()

    if not data:
        return jsonify({"error": "Meter not found"}), 404

    result = calculate_kw(energy)
    
    return jsonify({
        "meter": meter_number,
        "amount": result['amount'],
        "energy": energy,
        "vat": result['vat'],
        "debts": result['debts'],
    })

def calculate_kw(amount):
    # Example logic for calculation
    energy = amount / 10
    vat = amount * 0.15  #VAT calculation
    debts = amount * 0.1  #debts calculation
    return {
        "energy": energy,
        "vat": vat,
        "debts": debts
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

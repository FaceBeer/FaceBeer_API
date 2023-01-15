import json
import boto3
from decimal import Decimal


class DAO:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("leaderboard")
        tables = list(self.dynamodb.tables.all())
        print(tables)

    def create_table(self):
        self.dynamodb.create_table(
            TableName="leaderboard",
            KeySchema=[
                {'AttributeName': 'timestamp', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'timestamp', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={
                # ReadCapacityUnits set to 10 strongly consistent reads per second
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
            }
        )

    def delete_table(self):
        self.table.delete()

    def reset(self):
        self.delete_table()
        self.create_table()

    def add_item(self, name, bac, timestamp):
        self.table.put_item(Item={
            "name": name,
            "bac": bac,
            "timestamp": timestamp
        })

    def get_all_rows(self):
        response = self.table.scan()
        try:
            items = response["Items"]
            for i, row in enumerate(items):
                items[i]['bac'] = float(row['bac'])
            return items
        except KeyError:
            print("Scan failed")


if __name__ == "__main__":
    dao = DAO()
    dao.reset()
    # dao.create_table()
    # dao.add_item("Grant", Decimal(0.5), "11/30/2001")
    # dao.add_item("Grant", Decimal(0.5), "11/30/2002")
    print(*dao.get_all_rows(), sep='\n')

# Товары в корзине
bag = 10
bread = 15
apples = 50
all_items = [bag, bread, apples]
# Все доступные скидки
member_card = 10
student_ticket = 5
all_discounts = [member_card, student_ticket]


def sum_of_product_prices(products):
    return sum(products)


def apply_discounts_to_total(total, discounts):
    combined_discount = 0
    for disc in discounts:
        combined_discount += disc
    return total - total / 100 * combined_discount


total_price = sum_of_product_prices(all_items)
print(total_price)
price_after_discounts = apply_discounts_to_total(total_price, all_discounts)
print(price_after_discounts)

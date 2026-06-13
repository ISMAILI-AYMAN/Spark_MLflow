select
    order_id,
    count(*) as payment_count,
    sum(payment_value) as total_payment_value,
    max(case when payment_type = 'credit_card' then 1 else 0 end) as has_credit_card,
    max(case when payment_type = 'boleto' then 1 else 0 end) as has_boleto,
    max(case when payment_type = 'voucher' then 1 else 0 end) as has_voucher,
    max(case when payment_type = 'debit_card' then 1 else 0 end) as has_debit_card,
    max(payment_installments) as max_installments
from {{ ref('bronze_order_payments') }}
group by order_id

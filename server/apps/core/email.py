def create_collect_confirmation_email(
    first_name, title, description, target_amount, target_date
):
    """Создает сообщение, подтверждающее создание сбора"""
    email_message = f"""
                    Привет, {first_name}!

                    Вы только что создали новый сбор на нашей платформе.

                    Название вашего сбора: {title}
                    Детали вашего сбора: {description}
                    Сумма для сбора: {target_amount}

                    {
                    'Ориентировочная дата окончания сбора: ' + str(target_date)
                    if target_date
                    else 'Сбор является бессрочным.'
                    }

                    Спасибо за ваше участие!
                    """
    return email_message


def create_payment_confirmation_email(first_name, name, sum):
    """Создает сообщение, подтверждающее платеж на платформе"""
    email_message = f"""
                    Привет, {first_name}!

                    Ваш платеж успешно принят на нашей платформе.

                    Название сбора: {name}
                    Сумма платежа: {sum}


                    """
    return email_message

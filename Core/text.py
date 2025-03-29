from Core.Databases import info_settings, info_text

async def textInfo(str):
    text = {
        "info_vpn_command_text": f"{await info_text('info_vpn_command_text')} {await info_settings(2)}р",

        "buy_subscription_command_text": f"{await info_text('buy_subscription_command_text')}",

        "help_command_text": f"{await info_text('help_command_text')}",

        "payment_problems_text": f"{await info_text('payment_problems_text')}",

        "low_speed_problems" : f"{await info_text('low_speed_problems')}",

        "vpn_no_work" : f"{await info_text('vpn_no_work')}"
    }
    return text[str]
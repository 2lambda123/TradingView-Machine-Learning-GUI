import time
import numpy as np
from web_commands.commands import Functions
from TradeViewGUI import Main
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait


class ShortStoploss(Functions):
    """Find the best stop loss and take profit values for your strategy."""

    def __init__(self):
        Main.__init__(self)
        self.driver = self.create_driver()
        self.run_script()

    def run_script(self):
        # Load website with web driver.
        print("Loading script...\n")
        wait = WebDriverWait(self.driver, 15)
        self.get_webpage()

        # Ensure the Strategy Tester tab is clicked for proper automation.
        self.click_strategy_tester(wait)
        self.click_overview(wait)

        # Ensure we are on the Inputs tab and reset values to default settings.
        self.click_settings_button(wait)
        self.click_input_tab()
        self.click_enable_short_strategy_checkbox()
        self.click_reset_all_inputs(wait)
        self.click_ok_button()

        try:
            # Create a range variable.
            my_range = np.arange(
                float(self.minShortStoplossValue.text()),
                float(self.maxShortStoplossValue.text()),
                float(self.ShortIncrementValue.text()),
            )

            # Increment through the range.
            for number in my_range:
                count = round(number, 2)
                try:
                    self.click_settings_button(wait)
                    self.click_short_stoploss_input(count, wait)

                    # Allow time for webpage data refresh.
                    time.sleep(1)

                    self.get_net_profit_stoploss(count, wait)
                except (
                    StaleElementReferenceException,
                    TimeoutException,
                    NoSuchElementException,
                ) as error:
                    if error:
                        count -= 1
                        continue
        except ValueError:
            print(
                "\nValue Error: Ensure all text input boxes are filled with a number for proper script execution.\n"
            )
            return

        # Add the best parameters to the strategy.
        self.click_settings_button(wait)
        best_key = self.find_best_stoploss()
        self.click_short_stoploss_input(best_key, wait)
        self.driver.implicitly_wait(1)

        print("\n----------Results----------\n")
        self.click_overview(wait)
        self.print_best_stoploss()
        self.click_performance_summary(wait)
        self.print_total_closed_trades()
        self.print_net_profit()
        self.print_win_rate()
        self.print_max_drawdown()
        self.print_sharpe_ratio()
        self.print_sortino_ratio()
        self.print_win_loss_ratio()
        self.print_avg_win_trade()
        self.print_avg_loss_trade()
        self.print_avg_bars_in_winning_trades()
        # print("\n----------More Results----------\n")
        # self.print_gross_profit()
        # self.print_gross_loss()
        # self.print_buy_and_hold_return()
        # self.print_max_contracts_held()
        # self.print_open_pl()
        # self.print_commission_paid()
        # self.print_total_open_trades()
        # self.print_number_winning_trades()
        # self.print_number_losing_trades()
        # self.print_percent_profitable()
        # self.print_avg_trade()
        # self.print_avg_win_trade()
        # self.print_avg_loss_trade()
        # self.print_largest_winning_trade()
        # self.print_largest_losing_trade()
        # self.print_avg_bars_in_trades()
        # self.print_avg_bars_in_winning_trades()
        # self.print_avg_bars_in_losing_trades()
        # self.print_margin_calls()

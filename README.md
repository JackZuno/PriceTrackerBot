# AmazonPriceBot

## Content
The AmazonPriceBot is a Telegram bot designed to track price fluctuations of specific items. Users can add items to the bot's watchlist using the **/add** command, where the only required parameter is the item's URL. Currently, the bot supports online stores such as Amazon (tested with Amazon IT and UK), eBay (tested with eBay IT, UK, and USA), and the Lego Store.

Once items are added, they can be listed using the **/list** command. This command will display key details for each item, including its *name*, *initial price* at the time of addition, *date* of addition, and the *current price*. It will also show the *lowest* and *highest price* recorded, along with a clickable URL that directs to the product page.

Users can remove individual items or clear all items from their list through a specific button (or the **remove all** or the **remove item_name**). If the user want to cancel the operation, the bot provide a **cancel** button for easy exit. After an item is removed, the bot will delete any prior messages related to that item and notify the user whether the deletion was successful.

The bot also offers the option to **enable or disable notifications**. When notifications are enabled, the bot sends updates twice daily—once in the morning and once in the evening. These notifications include the same information as the **/list** command, but the bot will first check for any price changes and update the current price accordingly. If there are any changes in price, a new emoji is added to indicate the specific update.

If a user decides to disable notifications, the bot will stop sending updates about price changes. Additionally, if there are no items in the list, the bot will suggest disabling notifications.

If a user blocks the bot without first issuing the **/end** command, the bot will automatically stop sending messages after the first notification is sent following the block. The bot detects this situation through an exception triggered after a scheduled message fails to send due to the block from the user.

Finally, the **/help** command provides a list of all available commands in the bot.

## Usage Example

<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
  <figure style="text-align: center;">
    <img src="images/start.jpg" width="25%" />
    <figcaption>Start Bot</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/end_bot.jpg" width="25%" />
    <figcaption>Stop Bot</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/help.jpg" width="25%" />
    <figcaption>Help </figcaption>
  </figure>
</div>

<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
  <figure style="text-align: center;">
    <img src="images/add_item.jpg" width="25%" />
    <figcaption>Add Item</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/remove_pt1.jpg" width="25%" />
    <figcaption>Remove Part 1</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/remove_pt2.jpg" width="25%" />
    <figcaption>Remove Part 2</figcaption>
  </figure>
</div>

<div style="display: flex; justify-content: space-between;">
  <figure style="text-align: center;">
    <img src="images/enable_disable.jpg" width="25%" />
    <figcaption>Enable/Disable Notifications</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/notification_message.jpg" width="25%" />
    <figcaption>Notification Message</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/list.jpg" width="25%" />
    <figcaption>List all items</figcaption>
  </figure>
</div>


<!-- <div style="display: flex; justify-content: space-between;">
  <img src="images/start.jpg" width="30%" />
  <img src="images/end_bot.jpg" width="30%" />
  <img src="images/help.jpg" width="30%" />
</div>

<div style="display: flex; justify-content: space-between;">
  <img src="images/add_item.jpg" width="30%" />
  <img src="images/remove_pt1.jpg" width="30%" />
  <img src="images/remove_pt2.jpg" width="30%" />
</div>


<div style="display: flex; justify-content: space-between;">
  <img src="images/enable_disable.jpg" width="30%" />
  <img src="images/notification_message.jpg" width="30%" />
  <img src="images/list.jpg" width="30%" />
</div> -->

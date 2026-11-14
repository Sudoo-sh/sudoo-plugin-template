# Webhook alerts

Posts the alerts of your [Sudoo.sh](https://sudoo.sh) panel to a chat channel through an incoming webhook: Slack,
Mattermost, Rocket.Chat (Slack format) or Discord.

> This is the second example of the Sudoo.sh plugin template: a plugin with Python code behind an entry point,
> settings and a permission. It is a starting point, not a product. The notification group (`sudoo.notifications`)
> is planned for Sudoo.sh 2.0, so its interface may still change.

## Settings

| Setting | Default | Meaning |
| :--- | :--- | :--- |
| Webhook address | (empty) | The incoming-webhook address from your chat (https only). Empty: nothing is sent. Kept as a secret. |
| Send alerts from | `warning` | `info`, `success`, `warning` or `error`: alerts below this level are not sent. |
| Message format | `slack` | `slack` sends `{"text": ...}`; `discord` sends `{"content": ...}`. |

## What it sends

One message per alert, for example:

```
Error: Update of sales-main failed
git pull: merge conflict in addons/sale/models.py
https://panel.example.test/instances/sales-main
```

## Permissions

`network.outbound`: it connects to the webhook address you set, and nowhere else. Redirects are not followed.

## Licence

MIT, see LICENSE.md.

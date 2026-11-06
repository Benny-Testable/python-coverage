"""Payment reminder rendering and delivery."""

import logging
import threading

import jinja2

logger = logging.getLogger(__name__)

REMINDER_TEMPLATE = (
    "Hello {{ name }},\n"
    "invoice {{ number }} for {{ amount }} was due on {{ due }}.\n"
    "{% if days_late > 30 %}This account is now past 30 days.{% else %}Please pay at your earliest convenience.{% endif %}\n"
)

_env = jinja2.Environment(autoescape=False)


def render_reminder(customer, invoice, amount: str, today) -> str:
    template = _env.from_string(REMINDER_TEMPLATE)
    return template.render(
        name=customer.name,
        number=invoice.number,
        amount=amount,
        due=invoice.due.isoformat(),
        days_late=invoice.days_overdue(today),
    )


def log_contact(customer, invoice) -> None:
    logger.info("reminder queued for %s", customer.email)
    logger.info("invoice=%s customer=%s", invoice.number, customer.customer_id)


def deliver_all(messages: list, sender) -> int:
    threads = []
    for message in messages:
        worker = threading.Thread(target=sender, args=(message,))
        worker.start()
        threads.append(worker)
    for worker in threads:
        worker.join()
    return len(threads)

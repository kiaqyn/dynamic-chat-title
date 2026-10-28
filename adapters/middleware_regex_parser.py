#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Third-Party Middleware & OpenWebUI Outlet Filter for `dynamic-chat-title`
-----------------------------------------------------------------------------------
Extracts title updates emitted by `dynamic-chat-title` in either:
  1. Tier 2 HTML comment tag: <!-- dynamic-chat-title: 新标题 -->
  2. Tier 3/4 Advisory line:  💡 建议更新会话标题：「新标题」

Can be used standalone in any Python backend/gateway or pasted directly into
OpenWebUI -> Workspace -> Functions (as an Outlet Filter).
"""

import re
from typing import Optional, Tuple

TAG_PATTERN = re.compile(r"<!--\s*dynamic-chat-title:\s*(.+?)\s*-->")
ADVISORY_PATTERN = re.compile(r"💡\s*\*{0,2}建议更新会话标题\*{0,2}[：:]\s*「([^」\r\n]+)」")


def extract_dynamic_title(response_text: str, strip_tag: bool = True) -> Tuple[Optional[str], str]:
    """
    Parse an LLM response for a dynamic chat title update.
    Returns (extracted_title_or_None, cleaned_response_text).
    """
    title: Optional[str] = None
    cleaned = response_text

    tag_match = TAG_PATTERN.search(response_text)
    if tag_match:
        title = tag_match.group(1).strip()
        if strip_tag:
            cleaned = TAG_PATTERN.sub("", cleaned).rstrip()
        return title, cleaned

    adv_match = ADVISORY_PATTERN.search(response_text)
    if adv_match:
        title = adv_match.group(1).strip()

    return title, cleaned


class Filter:
    """
    Drop-in OpenWebUI / Third-Party Middleware Filter Class.
    Automatically detects title changes in the assistant's last message.
    """

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        messages = body.get("messages", [])
        if not messages:
            return body
        last_msg = messages[-1]
        if last_msg.get("role") == "assistant" and isinstance(last_msg.get("content"), str):
            new_title, cleaned_content = extract_dynamic_title(last_msg["content"], strip_tag=True)
            if new_title:
                last_msg["content"] = cleaned_content
                body["dynamic_chat_title"] = new_title
        return body

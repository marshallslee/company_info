SELECT co.company_group_id AS company_group_id, lang.code AS language_code, co.name
FROM company AS co
INNER JOIN company_group AS cg
ON co.company_group_id = cg.id
INNER JOIN language AS lang
ON co.language_id = lang.id
INNER JOIN company_tag AS ct
ON cg.id = ct.company_group_id
INNER JOIN (SELECT tag_group_id FROM tag WHERE name="tag_1") AS tg
ON ct.tag_group_id = tg.tag_group_id
ORDER BY co.company_group_id, co.name ASC;

{
				'name':	'Qltc	Quality	—	Supplier	Non-Conformance',
				'version':	'1.0.1',
				'category':	'Manufacturing/Quality',
				'summary':	'Record	and	track	supplier	non-conformances	through	to	closure.',
				'description':	"""
Supplier	Non-Conformance	Tracking
=================================
Records	defects	found	on	incoming	supplier	deliveries	and	tracks
corrective	actions	through	to	closure.
""",
				'author':	'Quantum	Leap	Trainers	and	Consultants',
				'website':	'https://peggingyouahead.qltc.in/',
				'license': 'LGPL-3',
				'depends': [
                   'base',
                   'mail',
                ],
                'data': [
                  'security/security.xml',
                  'security/ir.model.access.csv',
                  'data/mail_template.xml',
                  'views/quality_nc_views.xml',
                  'report/quality_nc_report.xml',
                ],
                'installable':	True,
				'application':	True,
				'auto_install':	False,
}

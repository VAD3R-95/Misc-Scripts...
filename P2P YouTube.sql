/* Standard Tables in SAP
   LFB1 - Vendor with CC
   LFA1 - Vendor Details
   EBAN - Purchase Requesition
   EKKO - PO header	 
   EKPO - PO Items
   EKBE - PO History
   EKET - Schedule Line Items
   RBKP - Invoice Header
   BKPF - Accounting Header
   BSAK - Cleared Items/Payments 
   BSIK - Open Items/Partial Payments
*/

select LFB1.LIFNR,  --LIFNR Vendor number
       LFB1.BUKRS,  -- Company code
       LFA1.NAME1 ,  -- NAME of Vendor
	   EBAN.BANFN,   -- PR Number
	   EBAN.AFNAM,    -- Requistioner
	   EKKO.EBELN,    -- PO Number
	   EKKO.ZTERM,    -- PO Pay Terms
	   EKPO.EBELP,    -- PO Item
	   EKPO.MATNR,     -- Material NUmbner
	   EKPO.TXZ01,     -- Description
	   EKPO.MENGE,     -- Ordered Quantity
	   EKPO.NETWR,      -- Total Value of Line Item
	   EKBE.BELNR,      -- Document Number
	   EKBE.BEWTP,       -- Indicator
	   EKBE.MENGE,       -- Quantity,
	   EKBE.DMBTR,        --Value in LC
	   EKBE.WRBTR,         --Value in DC
	   CASE WHEN EKBE.BEWTP = 'E' THEN 'GRN Doc.'
	        WHEN EKBE.BEWTP = 'Q' THEN 'IRN Doc.'
	   END AS 'Type of Doc.',
	   EKET.EINDT AS 'Del. Date',
	   EKET.MENGE AS 'Sch. Quantity',
	   EKET.WEMNG AS 'Del. Quanity',
	   EKET.MENGE - EKET.WEMNG AS 'Missing Qty',
	   RBKP.GJAHR AS 'Year of Invoice',
	   RBKP.ZBD1T as 'Invoice Pay Days',
	   RBKP.RMWWR as 'Total Invoice Value',
	   BKPF.BELNR AS 'Acc doc.',
	   BKPF.AWKEY AS 'Linkage',
	   BSAK.AUGDT as 'Clearing Date',
	   BSAK.AUGBL as 'Claring Doc.',
	   BSAK.DMBTR as 'Payment Value'
	   from LFB1 
       JOIN LFA1 on cast (LFB1.LIFNR AS VARCHAR) = CAST (LFA1.LIFNR AS VARCHAR)
	   JOIN EBAN ON EBAN.LIFNR = LFA1.LIFNR
	   JOIN EKKO ON EBAN.EBELN = EKKO.EBELN
	            AND LFB1.BUKRS = EKKO.BUKRS
	   JOIN EKPO ON EKKO.EBELN = EKPO.EBELN
	            AND EKKO.BUKRS = EKPO.BUKRS
	   JOIN EKBE ON EKPO.EBELN = EKBE.EBELN
	           AND  EKPO.EBELP = EKBE.EBELP
	   JOIN EKET ON EKPO.EBELN = EKET.EBELN 
	          AND EKPO.EBELP = EKET.EBELP
	   LEFT JOIN RBKP ON EKBE.BELNR = RBKP.BELNR
	          AND EKBE.BEWTP = 'Q'
	   LEFT JOIN BKPF ON AWKEY = CAST(RBKP.BELNR AS VARCHAR)+CAST (RBKP.GJAHR AS VARCHAR)
	   LEFT JOIN BSAK ON BKPF.BELNR = BSAK.BELNR
	                  AND LFA1.LIFNR =  BSAK.LIFNR 
					  AND BKPF.GJAHR = BSAK.GJAHR  
	   LEFT JOIN BSIK     ON BKPF.BELNR   =   BSIK.BELNR
	                  AND LFA1.LIFNR =  BSIK.LIFNR 
					  AND BKPF.GJAHR = BSIK.GJAHR   
	   WHERE LFA1.LIFNR = '113036'

	

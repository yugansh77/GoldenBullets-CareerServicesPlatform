export default async (req, res) => {
	try {
		// Get access token from authorization header
		const authHeader = req.headers.authorization
		if (!authHeader) {
			return res.status(401).json({ message: 'Authorization header missing' })
		}
		if (req.method === 'GET') {
			// Send GET request to fetch jobs by the current employer
			const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/jobs/employer`, {
				method: 'GET',
				headers: {
					Authorization: authHeader,
					'Content-Type': 'application/json',
				},
			})
			const data = await response.json()
			if (response.ok) {
				return res.status(200).json(data)
			}
		} else {
			return res.status(405).json({ message: 'Method not allowed' })
		}
	} catch (error) {
		console.error('Error accessing api/jobs', error)
		return res.status(403).json({ message: 'User forbidden' })
	}
}
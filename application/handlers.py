from httpx import AsyncClient
from aiohttp import web


async def get_user_info(request):

    email = request.query.get('email')
    password = request.query.get('password')

    api_path = 'https://api.comet.co/api/graphql'

    payload = {"operationName": "authenticate",
               "variables":
                   {'email': email, 'password': password, 'signupToken': 'null'},
               "query":
                   "mutation authenticate($email: EmailType!, $password: String!, $signupToken: String) "
                   "{\n  authenticate(email: $email, password: $password, signupToken: $signupToken) "
                   "{\n    id\n    ...User\n    __typename\n  }\n}\n\nfragment User on User "
                   "{\n  id\n  email\n  firstName\n  fullName\n  jobTitle\n  lastName\n  pendingActivation\n  "
                   "phoneNumber\n  profilePictureUrl\n  slackId\n  slackUsername\n  termsValidated\n  "
                   "termsValidatedAt\n  unreadChatMessagesCount\n  unseenMentionsCount\n  mentionsViewedAt\n  "
                   "corporate {\n    id\n    comments\n    companyId\n    role\n    token\n    missions {\n      "
                   "id\n      count\n      __typename\n    }\n    missionPendingRating {\n      id\n      "
                   "__typename\n    }\n    company {\n      id\n      skipTermsValidation\n      __typename\n    }\n    "
                   "__typename\n  }\n  freelance {\n    id\n    preUser\n    isInstructor\n    flaggedForQualif\n    "
                   "isFrozen\n    isQualified\n    acquisitionSource\n    availabilityDate\n    bankName\n    "
                   "bic\n    bitbucketUrl\n    callAvailability\n    gitHubUrl\n    gitlabUrl\n    iban\n    "
                   "isAvailable\n    isBillable\n    kaggleUrl\n    linkedInUrl\n    shouldUpdateAvailability\n    "
                   "maxDistance\n    prefContract\n    prefEnvironment\n    prefMobility\n    prefTime\n    "
                   "prefWorkplace\n    profileScore\n    publicId\n    referralCode\n    retribution\n    "
                   "retryDate\n    stackExchangeUrl\n    status\n    talentSuccessManagerId\n    twitterUrl\n    "
                   "websiteUrl\n    slackStatus\n    ...LinkedInImport\n    __typename\n  }\n  teamMember {\n    id\n    "
                   "accountManager\n    freelancerAgent\n    ...TeamMemberTip\n    __typename\n  }\n  impersonating "
                   "{\n    id\n    email\n    firstName\n    lastName\n    fullName\n    teamMember {\n      id\n      "
                   "__typename\n    }\n    __typename\n  }\n  ...FreelancerNavBar\n  ...UserFlags\n  "
                   "...CorporatePermissions\n  ...FreelancePermissions\n  __typename\n}\n\nfragment "
                   "TeamMemberTip on TeamMember {\n  id\n  tips\n  __typename\n}\n\nfragment UserFlags on "
                   "User {\n  id\n  corporate {\n    id\n    ...CorporateFlags\n    __typename\n  }\n  "
                   "freelance {\n    id\n    ...FreelancerFlags\n    __typename\n  }\n  __typename\n}\n\nfragment "
                   "CorporateFlags on Corporate {\n  id\n  flags {\n    id\n    ...Flag\n    __typename\n  }\n  "
                   "__typename\n}\n\nfragment Flag on Flag {\n  id\n  level\n  once\n  payload\n  permanent\n  "
                   "type\n  __typename\n}\n\nfragment FreelancerFlags on Freelance {\n  id\n  flags {\n    id\n    "
                   "...Flag\n    __typename\n  }\n  __typename\n}\n\nfragment FreelancerNavBar on User {\n  id\n  "
                   "slackId\n  profilePictureUrl\n  unreadChatMessagesCount\n  freelance {\n    id\n    status\n    "
                   "__typename\n  }\n  __typename\n}\n\nfragment CorporatePermissions on User {\n  id\n  permissions "
                   "{\n    id\n    showProfile\n    showMissions\n    showAdministration\n    showCommunity\n    "
                   "showCrew\n    __typename\n  }\n  __typename\n}\n\nfragment FreelancePermissions on User "
                   "{\n  id\n  permissions {\n    id\n    showProfile\n    showMissions\n    showStore\n    "
                   "showInfos\n    showExperiences\n    showQualification\n    showInstructor\n    "
                   "askForQualification\n    showPreferences\n    showCompany\n    __typename\n  }\n  "
                   "__typename\n}\n\nfragment LinkedInImport on Freelance {\n  id\n  fetchingLinkedIn\n  "
                   "lastLinkedInImport {\n    id\n    status\n    lastError\n    importedAt\n    __typename\n  }\n  "
                   "biography\n  user {\n    id\n    profilePictureUrl\n    jobTitle\n    __typename\n  }\n  "
                   "experienceInYears\n  experiences {\n    id\n    isCometMission\n    startDate\n    endDate\n    "
                   "companyName\n    description\n    location\n    skills {\n      id\n      name\n      primary\n      "
                   "freelanceExperienceSkillId\n      __typename\n    }\n    __typename\n  }\n  education {\n    id\n    "
                   "schoolName\n    degree\n    topic\n    description\n    startedIn\n    graduatedIn\n    "
                   "__typename\n  }\n  __typename\n}\n"
               }

    async with AsyncClient() as cli:

        response = await cli.post(api_path, json=payload)
        if response.status_code == 200:
            return web.Response(text=response.text)
        else:
            return web.Response(text="Email and password are required query parameters.", status=response.status_code)
